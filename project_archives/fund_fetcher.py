# -*- coding: UTF-8 -*-

import datetime
import re
import threading
from loguru import logger


class FundFetcher:
    
    def __init__(self, session, cache_map, csrf, result_list, sem):
        self.session = session
        self.CACHE_MAP = cache_map
        self._csrf = csrf
        self.result = result_list
        self.sem = sem
    
    def get_fund_forecast_growth(self, fund):
        try:
            fund_key = self.CACHE_MAP[fund]["fund_key"]
            url = "https://www.fund123.cn/api/fund/queryFundEstimateIntraday"
            params = {
                "_csrf": self._csrf
            }
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            data = {
                "startTime": today,
                "endTime": tomorrow,
                "limit": 200,
                "productId": fund_key,
                "format": True,
                "source": "WEALTHBFFWEB"
            }
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/json",
                "Origin": "https://www.fund123.cn",
                "Referer": "https://www.fund123.cn/fund",
                "User": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
            }
            response = self.session.post(url, headers=headers, params=params, json=data, timeout=10, verify=False)
            if response.json()["success"]:
                if response.json()["list"]:
                    fund_info = response.json()["list"][-1]
                    forecast_growth = str(round(float(fund_info["forecastGrowth"]) * 100, 2)) + "%"
                    return forecast_growth
            return "N/A"
        except Exception as e:
            logger.error(f"获取基金【{fund}】估值失败: {e}")
            return "N/A"
    
    def init_session(self):
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
    
    def add_code(self, codes):
        codes = codes.split(",")
        codes = [code.strip() for code in codes if code.strip()]
        for code in codes:
            try:
                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Origin": "https://www.fund123.cn",
                    "Referer": "https://www.fund123.cn/fund",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "X-API-Key": "foobar",
                    "accept": "json"
                }
                url = "https://www.fund123.cn/api/fund/searchFund"
                params = {
                    "_csrf": self._csrf
                }
                data = {
                    "fundCode": code
                }
                response = self.session.post(url, headers=headers, params=params, json=data, timeout=10, verify=False)
                if response.json()["success"]:
                    fund_key = response.json()["fundInfo"]["key"]
                    fund_name = response.json()["fundInfo"]["fundName"]
                    self.CACHE_MAP[code] = {
                        "fund_key": fund_key,
                        "fund_name": fund_name,
                        "is_hold": False
                    }
                    logger.info(f"添加基金代码【{code}】成功")
                else:
                    logger.error(f"添加基金代码【{code}】失败: {response.text.strip()}")
            except Exception as e:
                logger.error(f"添加基金代码【{code}】失败: {e}")
    
    def delete_code(self, codes):
        codes = codes.split(",")
        codes = [code.strip() for code in codes if code.strip()]
        for code in codes:
            try:
                if code in self.CACHE_MAP:
                    del self.CACHE_MAP[code]
                    logger.info(f"删除基金代码【{code}】成功")
                else:
                    logger.warning(f"删除基金代码【{code}】失败: 不存在该基金代码")
            except Exception as e:
                logger.error(f"删除基金代码【{code}】失败: {e}")
    
    def search_one_code(self, fund, fund_data, is_return, calculate_profit_loss_callback):
        with self.sem:
            try:
                fund_key = fund_data["fund_key"]
                fund_name = fund_data["fund_name"]

                headers = {
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Origin": "https://www.fund123.cn",
                    "Referer": "https://www.fund123.cn/fund",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "X-API-Key": "foobar",
                    "accept": "json"
                }
                url = f"https://www.fund123.cn/matiaria?fundCode={fund}"
                response = self.session.get(url, headers=headers, timeout=10, verify=False)
                dayOfGrowth = re.findall('\"dayOfGrowth\"\:\"(.*?)\"', response.text)[0]
                dayOfGrowth = str(round(float(dayOfGrowth), 2)) + "%"

                netValueDate = re.findall('\"netValueDate\"\:\"(.*?)\"', response.text)[0]
                currentNetValue = re.findall('\"currentNetValue\"\:\"(.*?)\"', response.text)
                currentNetValue = float(currentNetValue[0]) if currentNetValue else 0.0
                
                dayGrowthValue = dayOfGrowth
                if is_return:
                    dayOfGrowth = f"{dayOfGrowth}({netValueDate})"

                url = "https://www.fund123.cn/api/fund/queryFundQuotationCurves"
                params = {
                    "_csrf": self._csrf
                }
                data = {
                    "productId": fund_key,
                    "dateInterval": "ONE_MONTH"
                }
                response = self.session.post(url, headers=headers, params=params, json=data, timeout=10, verify=False)
                if not response.json()["success"]:
                    logger.error(f"查询基金代码【{fund}】失败: {response.text.strip()}")
                    return
                points = response.json()["points"]
                points = [x for x in points if x["type"] == "fund"]

                montly_growth = []
                last_rate = None
                for point in points:
                    if last_rate is None:
                        last_rate = point["rate"]
                        continue
                    now_rate = point["rate"]
                    if now_rate >= last_rate:
                        montly_growth.append(f"涨,{now_rate}")
                    else:
                        montly_growth.append(f"跌,{now_rate}")
                    last_rate = now_rate

                montly_growth = montly_growth[::-1]
                montly_growth_day = sum(1 for x in montly_growth if x[0] == "涨")
                montly_growth_day_count = len(montly_growth)
                consecutive_count = 1
                start_rate = montly_growth[0].split(",")[1]
                montly_growth_rate = str(round(round(float(start_rate), 4) * 100, 2)) + "%"
                end_rate = 0
                for i in montly_growth[1:]:
                    if i[0] == montly_growth[0][0]:
                        consecutive_count += 1
                    else:
                        end_rate = i.split(",")[1]
                        break

                montly_growth_day = str(montly_growth_day)
                if "-" in montly_growth_rate:
                    if not is_return:
                        montly_growth_day = "\033[1;32m" + montly_growth_day
                else:
                    if not is_return:
                        montly_growth_day = "\033[1;31m" + montly_growth_day

                consecutive_growth = str(round(round(float(start_rate) - float(end_rate), 4) * 100, 2)) + "%"
                if montly_growth[0][0] == "跌":
                    if not is_return:
                        consecutive_count = "\033[1;32m" + str(-consecutive_count)
                        consecutive_growth = "\033[1;32m" + str(consecutive_growth)
                    else:
                        consecutive_count = str(-consecutive_count)
                        consecutive_growth = str(consecutive_growth)
                else:
                    if not is_return:
                        consecutive_count = "\033[1;31m" + str(consecutive_count)
                        consecutive_growth = "\033[1;31m" + str(consecutive_growth)
                    else:
                        consecutive_count = str(consecutive_count)
                        consecutive_growth = str(consecutive_growth)

                url = "https://www.fund123.cn/api/fund/queryFundEstimateIntraday"
                params = {
                    "_csrf": self._csrf
                }
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                data = {
                    "startTime": today,
                    "endTime": tomorrow,
                    "limit": 200,
                    "productId": fund_key,
                    "format": True,
                    "source": "WEALTHBFFWEB"
                }
                response = self.session.post(url, headers=headers, params=params, json=data, timeout=10, verify=False)
                if response.json()["success"]:
                    if not response.json()["list"]:
                        now_time = "N/A"
                        forecastGrowth = "N/A"
                    else:
                        fund_info = response.json()["list"][-1]
                        now_time = datetime.datetime.fromtimestamp(fund_info["time"] / 1000).strftime(
                            "%H:%M:%S"
                        )
                        forecastGrowth = str(round(float(fund_info["forecastGrowth"]) * 100, 2)) + "%"
                        if not is_return:
                            if "-" in forecastGrowth:
                                forecastGrowth = "\033[1;32m" + forecastGrowth
                            else:
                                forecastGrowth = "\033[1;31m" + forecastGrowth
                    if not is_return:
                        if "-" in dayOfGrowth:
                            dayOfGrowth = "\033[1;32m" + dayOfGrowth
                        else:
                            dayOfGrowth = "\033[1;31m" + dayOfGrowth
                    if not is_return:
                        if self.CACHE_MAP[fund].get("is_hold", False):
                            fund_name = "⭐ " + fund_name
                        sectors = self.CACHE_MAP[fund].get("sectors", [])
                        if sectors:
                            sector_str = ",".join(sectors)
                            fund_name = f"({sector_str}) {fund_name}"
                    consecutive_info = f"{consecutive_count}天 {consecutive_growth}"
                    monthly_info = f"{montly_growth_day}/{montly_growth_day_count} {montly_growth_rate}"

                    hold_amount = self.CACHE_MAP[fund].get("temp_amount", 0.0)
                    hold_display = f"{hold_amount:.2f}" if hold_amount > 0 else ""
                    profit_loss = calculate_profit_loss_callback(hold_amount, forecastGrowth)
                    
                    if not is_return and profit_loss:
                        if profit_loss.startswith("+"):
                            profit_loss = "\033[1;31m" + profit_loss
                        else:
                            profit_loss = "\033[1;32m" + profit_loss
                    
                    valuation = hold_amount + float(profit_loss.replace("+", "").replace("-", "")) if profit_loss else hold_amount
                    valuation_display = f"{valuation:.2f}" if valuation > 0 else ""

                    self.result.append([
                        fund, fund_name, now_time, forecastGrowth, dayOfGrowth, consecutive_info, monthly_info, hold_display, profit_loss, valuation_display
                    ])
                else:
                    logger.error(f"查询基金代码【{fund}】失败: {response.text.strip()}")
            except Exception as e:
                logger.error(f"查询基金代码【{fund}】失败: {e}")
