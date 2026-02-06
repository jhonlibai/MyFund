# -*- coding: UTF-8 -*-

import argparse
import json
import os
import re
import threading
import time

import requests
import urllib3
from curl_cffi import requests as curl_requests
from dotenv import load_dotenv
from loguru import logger
from tabulate import tabulate

from ai_analyzer import AIAnalyzer
from fund_calculator import FundCalculator
from fund_fetcher import FundFetcher
from fund_manager import FundManager, MAJOR_CATEGORIES
from fund_html import FundHTML
from market_fetcher import MarketFetcher
from module_html import get_table_html

load_dotenv()

sem = threading.Semaphore(5)

urllib3.disable_warnings()
urllib3.util.ssl_.DEFAULT_CIPHERS = ":".join(
    [
        "ECDHE+AESGCM",
        "ECDHE+CHACHA20",
        'ECDHE-RSA-AES128-SHA',
        'ECDHE-RSA-AES256-SHA',
        "RSA+AESGCM",
        'AES128-SHA',
        'AES256-SHA',
    ]
)
tabulate.PRESERVE_WHITESPACE = True


def format_table_msg(table, tablefmt="pretty"):
    return tabulate(table, tablefmt=tablefmt, missingval="N/A")


class MaYiFund:
    CACHE_MAP = {}
    MAJOR_CATEGORIES = MAJOR_CATEGORIES

    def __init__(self):
        self.session = requests.Session()
        self.baidu_session = curl_requests.Session(impersonate="chrome")
        self._csrf = ""
        self.report_dir = None
        self.load_cache()
        self.init()
        self.result = []
        
        self.calculator = FundCalculator(
            cache_map=self.CACHE_MAP,
            save_cache_callback=self.save_cache,
            get_fund_forecast_callback=self.get_fund_forecast_growth
        )
        
        self.fetcher = FundFetcher(
            session=self.session,
            cache_map=self.CACHE_MAP,
            csrf=self._csrf,
            result_list=self.result,
            sem=sem
        )
        
        self.manager = FundManager(
            session=self.session,
            cache_map=self.CACHE_MAP,
            csrf=self._csrf,
            save_cache_callback=self.save_cache,
            format_table_callback=format_table_msg
        )
        
        self.market_fetcher = MarketFetcher(baidu_session=self.baidu_session)
        
        self.fund_html_module = FundHTML(
            cache_map=self.CACHE_MAP,
            search_code_callback=self.search_code,
            major_categories=self.MAJOR_CATEGORIES
        )

    def load_cache(self):
        if not os.path.exists("cache"):
            os.mkdir("cache")
        if os.path.exists("cache/fund_map.json"):
            with open("cache/fund_map.json", "r", encoding="utf-8") as f:
                self.CACHE_MAP = json.load(f)

    def save_cache(self):
        with open("cache/fund_map.json", "w", encoding="utf-8") as f:
            json.dump(self.CACHE_MAP, f, ensure_ascii=False, indent=4)

    def init(self):
        res = self.session.get("https://www.fund123.cn/fund", headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }, timeout=10, verify=False)
        self._csrf = re.findall('\"csrf\":\"(.*?)\"', res.text)[0]

        self.baidu_session.get("https://gushitong.baidu.com/index/ab-000001", headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "referer": "https://gushitong.baidu.com/"
        }, timeout=10, verify=False)

    def get_fund_forecast_growth(self, fund):
        return self.fetcher.get_fund_forecast_growth(fund)

    def search_one_code(self, fund, fund_data, is_return):
        self.fetcher.search_one_code(fund, fund_data, is_return, self.calculator.calculate_profit_loss)

    def search_code(self, is_return=False):
        self.result.clear()
        threads = []
        for fund, fund_data in self.CACHE_MAP.items():
            if fund in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate"]:
                continue
            t = threading.Thread(target=self.search_one_code, args=(fund, fund_data, is_return))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        logger.debug(f"search_code: is_return={is_return}, result_count={len(self.result)}")
        if is_return:
            self.result = sorted(
                self.result,
                key=lambda x: float(x[3].replace("%", "")) if x[3] != "N/A" else -99,
                reverse=True
            )
            logger.debug(f"search_code: sorted result_count={len(self.result)}")
            return self.result
        if self.result:
            self.result = sorted(
                self.result,
                key=lambda x: float(x[3].split("m")[1].replace("%", "")) if x[3] != "N/A" else -99,
                reverse=True
            )
            logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 基金估值信息:")
            for line_msg in format_table_msg([
                [
                    "基金代码", "基金名称", "估值时间", "估值", "日涨幅", "连涨/跌", "近30天", "持有", "盈亏"
                ],
                *self.result
            ]).split("\n"):
                logger.info(line_msg)
            
            total_hold = 0.0
            total_profit_loss = 0.0
            for row in self.result:
                hold_str = row[7]
                profit_loss_str = row[8]
                if hold_str:
                    try:
                        total_hold += float(hold_str)
                    except ValueError:
                        pass
                if profit_loss_str:
                    try:
                        clean_profit_loss_str = profit_loss_str
                        if "\033" in clean_profit_loss_str:
                            parts = clean_profit_loss_str.split("\033")
                            clean_profit_loss_str = parts[-1] if len(parts) > 1 else parts[0]
                        matches = re.findall(r'-?\d+\.?\d*', clean_profit_loss_str)
                        if matches:
                            clean_profit_loss_str = matches[-1]
                        profit_loss_value = float(clean_profit_loss_str)
                        total_profit_loss += profit_loss_value
                    except ValueError:
                        pass
            
            if total_hold > 0:
                total_profit_display = f"+{total_profit_loss:.2f}" if total_profit_loss >= 0 else f"{total_profit_loss:.2f}"
                logger.info(f"总持仓: {total_hold:.2f}元, 总盈亏: {total_profit_display}元")
            
            self.CACHE_MAP["total_hold_amount"] = total_hold
            self.CACHE_MAP["total_profit_loss"] = total_profit_loss
            self.save_cache()
            
            self.calculator.calculate_total_holdings_valuation()
            self.calculator.update_temp_amount_during_trading_hours()
            self.calculator.update_hold_amount_after_market_close()

    def fund_html(self):
        return self.fund_html_module.fund_html()

    def select_fund_html(self, bk_id=None):
        return self.fund_html_module.select_fund_html(bk_id)

    def select_fund(self, bk_id=None, is_return=False):
        return FundHTML.select_fund(bk_id, is_return)

    def get_market_info(self, is_return=False):
        return self.market_fetcher.get_market_info(is_return)

    def marker_html(self):
        return self.market_fetcher.marker_html()

    def gold(self, is_return=False):
        return self.market_fetcher.gold(is_return)

    def gold_html(self):
        return self.market_fetcher.gold_html()

    def bk(self, is_return=False):
        return self.market_fetcher.bk(is_return)

    def bk_html(self):
        return self.market_fetcher.bk_html()

    def kx(self, is_return=False, count=10):
        return self.market_fetcher.kx(is_return, count)

    def kx_html(self):
        return self.market_fetcher.kx_html()

    def real_time_gold(self, is_return=False):
        return self.market_fetcher.real_time_gold(is_return)

    def real_time_gold_html(self):
        return self.market_fetcher.real_time_gold_html()

    def A(self, is_return=False):
        return self.market_fetcher.A(is_return)

    def A_html(self):
        return self.market_fetcher.A_html()

    def seven_A(self, is_return=False):
        return self.market_fetcher.seven_A(is_return)

    def seven_A_html(self):
        return self.market_fetcher.seven_A_html()

    def add_code(self, codes):
        self.manager.add_code(codes)
        self.save_cache()

    def delete_code(self, codes):
        self.manager.delete_code(codes)
        self.save_cache()

    def mark_fund_sector(self):
        self.manager.mark_fund_sector()
        self.save_cache()

    def unmark_fund_sector(self):
        self.manager.unmark_fund_sector()
        self.save_cache()

    def set_hold_amount(self, set_hold_amount):
        self.manager.set_hold_amount(set_hold_amount)
        self.save_cache()

    def set_cost_price(self, set_cost_price):
        self.manager.set_cost_price(set_cost_price)
        self.save_cache()

    def toggle_hold(self, codes):
        self.manager.toggle_hold(codes)
        self.save_cache()

    def toggle_not_hold(self, codes):
        self.manager.toggle_not_hold(codes)
        self.save_cache()

    def ai_analysis(self, deep_mode=False, fast_mode=False):
        analyzer = AIAnalyzer()
        if deep_mode:
            analyzer.analyze_deep(self, report_dir=self.report_dir)
        elif fast_mode:
            analyzer.analyze_fast(self, report_dir=self.report_dir)
        else:
            analyzer.analyze(self, report_dir=self.report_dir)

    def run(self, is_add=False, is_delete=False, is_hold=False, is_not_hold=False, report_dir=None,
            deep_mode=False, fast_mode=False, with_ai=False, select_mode=False, mark_sector=False, unmark_sector=False, 
            set_hold_amount=None, set_cost_price=None):

        if select_mode:
            self.select_fund()
            return

        if mark_sector:
            self.mark_fund_sector()
            return

        if unmark_sector:
            self.unmark_fund_sector()
            return

        if set_hold_amount:
            self.set_hold_amount(set_hold_amount)
            return

        if set_cost_price:
            self.set_cost_price(set_cost_price)
            return

        self.report_dir = report_dir

        if not self.CACHE_MAP:
            logger.warning("暂无缓存代码信息, 请先添加基金代码")
            is_add = True
            is_delete = False
            is_hold = False
            is_not_hold = False

        if is_not_hold:
            hold_codes = [code for code, data in self.CACHE_MAP.items() if data.get("is_hold", False)]
            if not hold_codes:
                logger.warning("暂无持有标注基金代码")
                return
            logger.debug(f"当前持有标注基金代码: {hold_codes}")
            logger.debug("请输入基金代码, 多个基金代码以英文逗号分隔:")
            codes = input()
            self.toggle_not_hold(codes)
            return

        if is_hold:
            hold_codes = [code for code, data in self.CACHE_MAP.items() if data.get("is_hold", False)]
            if not hold_codes:
                logger.warning("暂无持有标注基金代码")
                return
            logger.debug(f"当前持有标注基金代码: {hold_codes}")
            logger.debug("请输入基金代码, 多个基金代码以英文逗号分隔:")
            codes = input()
            self.toggle_hold(codes)
            return

        if is_add:
            logger.debug("请输入基金代码, 多个基金代码以英文逗号分隔:")
            codes = input()
            self.add_code(codes)
            return

        if is_delete:
            logger.debug("请输入基金代码, 多个基金代码以英文逗号分隔:")
            codes = input()
            self.delete_code(codes)
            return

        if with_ai:
            self.ai_analysis(deep_mode=deep_mode, fast_mode=fast_mode)
            return

        self.search_code()
        self.get_market_info()
        self.gold()
        self.bk()
        self.kx()
        self.real_time_gold()
        self.A()
        self.seven_A()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MaYiFund')
    parser.add_argument('-a', '--add', action='store_true', help='添加基金代码')
    parser.add_argument("-d", "--delete", action="store_true", help="删除基金代码")
    parser.add_argument("-c", "--hold", action="store_true", help="添加持有基金标注")
    parser.add_argument("-b", "--not_hold", action="store_true", help="删除持有基金标注")
    parser.add_argument("-e", "--mark_sector", action="store_true", help="标记板块")
    parser.add_argument("-u", "--unmark_sector", action="store_true", help="删除标记板块")
    parser.add_argument("-s", "--select", action="store_true", help="选择板块查看基金列表")
    parser.add_argument("-o", "--output", type=str, nargs='?', const="reports", default=None,
                        help="输出AI分析报告到指定目录（默认: reports）。只有使用此参数时才会保存报告文件")
    parser.add_argument("-f", "--fast", action="store_true", help="启用快速分析模式")
    parser.add_argument("-D", "--deep", action="store_true", help="启用深度研究模式")
    parser.add_argument("-W", "--with-ai", action="store_true", help="AI分析")
    parser.add_argument("--set-hold-amount", type=str, help="设置基金持有金额，格式：基金代码=金额，多个用逗号分隔，如：025209=7548.81")
    parser.add_argument("--set-cost-price", type=str, help="设置基金买入成本价，格式：基金代码=成本价，多个用逗号分隔，如：025209=1.2345")
    args = parser.parse_args()

    mayi_fund = MaYiFund()
    report_dir = args.output if args.output is not None else None
    mayi_fund.run(args.add, args.delete, args.hold, args.not_hold, report_dir, args.deep, args.fast, args.with_ai, args.select, args.mark_sector, args.unmark_sector, args.set_hold_amount, args.set_cost_price)
