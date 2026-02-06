# -*- coding: UTF-8 -*-

import datetime
import json
import re
import requests
import time
from curl_cffi import requests as curl_requests
from loguru import logger
from module_html import get_table_html
from tabulate import tabulate


def format_table_msg(table, tablefmt="pretty"):
    return tabulate(table, tablefmt=tablefmt, missingval="N/A")


class MarketFetcher:
    
    def __init__(self, baidu_session):
        self.baidu_session = baidu_session
        self.setup_baidu_session()
    
    def setup_baidu_session(self):
        self.baidu_session.headers = {
            "accept": "application/vnd.finance-web.v1+json",
            "accept-language": "zh-CN,zh;q=0.9",
            "acs-token": "1767852006302_1767922774428_a5+nkAvkUigC1QCMVgphVfGSz3uvhigDZkrDM9ew7wjpNrUkQBUNgD3XpM57f2mcq/IePhZEI0fKkiKL/rXshBM3uF81xTcvjPL2PJay3YltapNyRHEYepcudaTSLNXVISph2tImkqnH1JNad7RLtMr2hm8AJJ+vhxll2W7WfAVn0E+PWLFAPJFlOXmuhwETtOtD+gKWTCEPavgdP7hrdfKtIUC8Cty6G96gY+5o9w/VYOdGnqyX8fUOV1i5ieJRaGP9N16M/nSxa5+y0oMluHENQs4DtkKzZdVgG16K8tobJVNk0Gq/kd+q782nVNrulOZn1qhNVGH6uTJUnZwnmyhnlimAtOB7vzSri3r5ut38GAeb6Svp4kw4M6lQZE6LUlNm9ZStZV1QPEmoS9l3ow==",
            "origin": "https://gushitong.baidu.com",
            "priority": "u=1, i",
            "referer": "https://gushitong.baidu.com/",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
    
    def get_market_info(self, is_return=False):
        result = []
        try:
            markets = ["asia", "america"]
            for market in markets:
                url = f"https://finance.pae.baidu.com/api/getbanner?market={market}&finClientType=pc"
                response = self.baidu_session.get(url, timeout=10, verify=False)
                if response.json()["ResultCode"] == "0":
                    market_list = response.json()["Result"]["list"]
                    for market_info in market_list:
                        ratio = market_info["ratio"]
                        if not is_return:
                            if "-" in ratio:
                                ratio = "\033[1;32m" + ratio
                            else:
                                ratio = "\033[1;31m" + ratio
                        result.append([
                            market_info["name"],
                            market_info["lastPrice"],
                            ratio
                        ])

            url = "https://finance.pae.baidu.com/vapi/v1/getquotation"
            params = {
                "srcid": "5353",
                "all": "1",
                "pointType": "string",
                "group": "quotation_index_minute",
                "query": "399006",
                "code": "399006",
                "market_type": "ab",
                "newFormat": "1",
                "name": "创业板指",
                "finClientType": "pc"
            }
            response = self.baidu_session.get(url, params=params, timeout=10, verify=False)
            if str(response.json()["ResultCode"]) == "0":
                cur = response.json()["Result"]["cur"]
                ratio = cur["ratio"]
                if not is_return:
                    if "-" in ratio:
                        ratio = "\033[1;32m" + ratio
                    else:
                        ratio = "\033[1;31m" + ratio
                result.insert(2, [
                    "创业板指",
                    cur["price"],
                    ratio
                ])
        except Exception as e:
            logger.error(f"获取市场信息失败: {e}")
        if is_return:
            return result
        if result:
            logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 市场信息:")
            for line_msg in format_table_msg([
                [
                    "指数名称", "指数", "涨跌幅"
                ],
                *result
            ]).split("\n"):
                logger.info(line_msg)
    
    def marker_html(self):
        result = self.get_market_info(True)
        return get_table_html(
            ["指数名称", "指数", "涨跌幅"],
            result,
        )
    
    @staticmethod
    def gold(is_return=False):
        try:
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9",
                "referer": "https://quote.cngold.org/gjs/swhj_zghj.html",
                "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "script",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            }
            url = "https://api.jijinhao.com/quoteCenter/history.htm"
            params = {
                "code": "JO_52683",
                "style": "3",
                "pageSize": "10",
                "needField": "128,129,70",
                "currentPage": "1",
                "_": int(time.time() * 1000)
            }
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
            data = json.loads(response.text.replace("var quote_json = ", ""))["data"]

            url = "https://api.jijinhao.com/quoteCenter/history.htm"
            params = {
                "code": "JO_42660",
                "style": "3",
                "pageSize": "10",
                "needField": "128,129,70",
                "currentPage": "1",
                "_": int(time.time() * 1000)
            }
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
            data2 = json.loads(response.text.replace("var quote_json = ", ""))["data"]

            gold_list = []

            for i in range(len(data)):
                gold = data[i]
                t = gold["time"]
                date = datetime.datetime.fromtimestamp(t / 1000).strftime("%Y-%m-%d")
                radio = str(gold.get("q70", "N/A"))
                radio2 = "N/A"
                gold2 = {}
                if len(data2) > i:
                    gold2 = data2[i]
                    radio2 = str(gold.get("q70", "N/A"))
                if not is_return:
                    if "-" in radio:
                        radio = "\033[1;32m" + radio
                    else:
                        radio = "\033[1;31m" + radio
                    if "-" in radio2:
                        radio2 = "\033[1;32m" + radio2
                    else:
                        radio2 = "\033[1;31m" + radio2
                gold_list.append([
                    date,
                    gold["q1"],
                    gold2.get("q1", "N/A"),
                    radio,
                    radio2
                ])
            if is_return:
                return gold_list[::-1]
            if gold_list:
                logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 金价:")
                for line_msg in format_table_msg([
                    [
                        "日期", "中国黄金基础金价", "周大福金价", "中国黄金基础金价涨跌", "周大福金价涨跌"
                    ],
                    *gold_list[::-1]
                ]).split("\n"):
                    logger.info(line_msg)
        except Exception as e:
            logger.error(f"获取贵金属价格失败: {e}")
    
    def gold_html(self):
        result = self.gold(True)
        if result:
            return get_table_html(
                ["日期", "中国黄金基础金价", "周大福金价", "中国黄金基础金价涨跌", "周大福金价涨跌"],
                result
            )
    
    @staticmethod
    def bk(is_return=False):
        bk_result = []
        try:
            url = "https://push2.eastmoney.com/api/qt/clist/get"
            params = {
                "cb": "",
                "fid": "f62",
                "po": "1",
                "pz": "100",
                "pn": "1",
                "np": "1",
                "fltt": "2",
                "invt": "2",
                "ut": "8dec03ba335b81bf4ebdf7b29ec27d15",
                "fs": "m:90 t:2",
                "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13"
            }
            response = requests.get(url, params=params, timeout=10, verify=False)
            if str(response.json()["data"]):
                data = response.json()["data"]
                for bk in data["diff"]:
                    ratio = str(bk["f3"]) + "%"
                    if not is_return:
                        if "-" in ratio:
                            ratio = "\033[1;32m" + ratio
                        else:
                            ratio = "\033[1;31m" + ratio
                    add_market_cap = bk["f62"]
                    add_market_cap = str(round(add_market_cap / 100000000, 2)) + "亿"
                    if not is_return:
                        if "-" in add_market_cap:
                            add_market_cap = "\033[1;32m" + add_market_cap
                        else:
                            add_market_cap = "\033[1;31m" + add_market_cap
                    add_market_cap2 = bk["f84"]
                    add_market_cap2 = str(round(add_market_cap2 / 100000000, 2)) + "亿"
                    if not is_return:
                        if "-" in add_market_cap2:
                            add_market_cap2 = "\033[1;32m" + add_market_cap2
                        else:
                            add_market_cap2 = "\033[1;31m" + add_market_cap2
                    bk_result.append([
                        bk["f14"],
                        ratio,
                        add_market_cap,
                        str(round(bk["f184"], 2)) + "%",
                        add_market_cap2,
                        str(round(bk["f87"], 2)) + "%",
                    ])
        except:
            pass

        bk_result = sorted(
            bk_result,
            key=lambda x: float(x[1].split("m")[-1].replace("%", "")) if x[3] != "N/A" else -99,
            reverse=True
        )
        if is_return:
            return bk_result
        if bk_result:
            logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 行业板块:")
            for line_msg in format_table_msg([
                [
                    "板块名称", "今日涨跌幅", "今日主力净流入", "今日主力净流入占比", "今日小单净流入", "今日小单流入占比"
                ],
                *bk_result
            ]).split("\n"):
                logger.info(line_msg)
    
    def bk_html(self):
        result = self.bk(True)
        return get_table_html(
            ["板块名称", "今日涨跌幅", "今日主力净流入", "今日主力净流入占比", "今日小单净流入", "今日小单流入占比"],
            result,
            sortable_columns=[1, 2, 3, 4, 5]
        )
    
    def kx(self, is_return=False, count=10):
        url = f"https://finance.pae.baidu.com/selfselect/expressnews?rn={count}&pn=0&tag=A股&finClientType=pc"
        kx_list = []
        try:
            response = self.baidu_session.get(url, timeout=10, verify=False)
            if response.json()["ResultCode"] == "0":
                kx_list = response.json()["Result"]["content"]["list"]
        except:
            pass

        if is_return:
            return kx_list

        if kx_list:
            logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 7*24 快讯:")
            for i, v in enumerate(kx_list):
                evaluate = v.get("evaluate", "")
                if evaluate == "利好":
                    pre = "\033[1;31m"
                elif evaluate == "利空":
                    pre = "\033[1;32m"
                else:
                    pre = ""
                title = v.get("title", v["content"]["items"][0]["data"])
                publish_time = v["publish_time"]
                publish_time = datetime.datetime.fromtimestamp(int(publish_time)).strftime("%Y-%m-%d %H:%M:%S")
                entity = v.get("entity", [])
                entity = ", ".join([f"{x['code'].strip()}-{x['name'].strip()} {x['ratio'].strip()}" for x in entity])
                logger.info(f"{pre}{i + 1}. {publish_time} {title}.")
                if entity:
                    logger.debug(f"影响股票: {entity}.")
    
    def kx_html(self):
        result = self.kx(True)
        table_data = []
        for v in result:
            evaluate = v.get("evaluate", "")
            title = v.get("title", v["content"]["items"][0]["data"])
            publish_time = v["publish_time"]
            publish_time = datetime.datetime.fromtimestamp(int(publish_time)).strftime("%H:%M:%S")
            if evaluate == "利好":
                evaluate = f'<span class="positive">{evaluate}</span>'
            elif evaluate == "利空":
                evaluate = f'<span class="negative">{evaluate}</span>'
            table_data.append([publish_time, evaluate, title])
        return get_table_html(
            ["时间", "多空", "快讯内容"],
            table_data
        )
    
    @staticmethod
    def real_time_gold(is_return=False):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "referer": "https://quote.cngold.org/gjs/gjhj.html",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "sec-fetch-storage-access": "active",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }
        try:
            url = "https://api.jijinhao.com/quoteCenter/realTime.htm"
            params = {
                "codes": "JO_71,JO_92233,JO_92232,JO_75",
                "_": str(int(time.time() * 1000))
            }
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
            data = json.loads(response.text.replace("var quote_json = ", ""))
            result = [[], [], []]
            columns = ["名称", "最新价", "涨跌额", "涨跌幅", "开盘价", "最高价", "最低价", "昨收价", "更新时间", "单位"]
            if data:
                data1 = data["JO_71"]
                data2 = data["JO_92233"]
                data3 = data["JO_92232"]
                keys = ["showName", "q63", "q70", "q80", "q1", "q3", "q4", "q2", "time", "unit"]
                for key in keys:
                    if key == "time":
                        for i, t in enumerate([data1[key], data2[key], data3[key]]):
                            date = datetime.datetime.fromtimestamp(t / 1000).strftime("%Y-%m-%d %H:%M:%S")
                            result[i].append(date)

                    else:
                        value1 = data1.get(key, "N/A")
                        value2 = data2.get(key, "N/A")
                        value3 = data3.get(key, "N/A")
                        if not isinstance(value1, str):
                            value1 = round(value1, 2)
                        if not isinstance(value2, str):
                            value2 = round(value2, 2)
                        if not isinstance(value3, str):
                            value3 = round(value3, 2)
                        value1 = str(value1)
                        value2 = str(value2)
                        value3 = str(value3)
                        if key == "q70":
                            if not is_return:
                                if "-" in value1:
                                    value1 = "\033[1;32m" + value1
                                else:
                                    value1 = "\033[1;31m" + value1
                                if "-" in value2:
                                    value2 = "\033[1;32m" + value2
                                else:
                                    value2 = "\033[1;31m" + value2
                                if "-" in value3:
                                    value3 = "\033[1;32m" + value3
                                else:
                                    value3 = "\033[1;31m" + value3
                        if key == "q80":
                            value1 = value1 + "%"
                            value2 = value2 + "%"
                            value3 = value3 + "%"
                        result[0].append(value1)
                        result[1].append(value2)
                        result[2].append(value3)

            if is_return:
                return result
            if result and result[0] and result[1] and result[2]:
                logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 实时贵金属价:")
                for line_msg in format_table_msg([
                    columns,
                    result[0],
                    result[1],
                    result[2]
                ]).split("\n"):
                    logger.info(line_msg)
        except Exception as e:
            logger.error(f"获取实时贵金属价格失败: {e}")
    
    def real_time_gold_html(self):
        result = self.real_time_gold(True)
        if result:
            return get_table_html(
                ["名称", "最新价", "涨跌额", "涨跌幅", "开盘价", "最高价", "最低价", "昨收价", "更新时间", "单位"],
                result
            )
    
    def A(self, is_return=False):
        url = "https://finance.pae.baidu.com/vapi/v1/getquotation"
        params = {
            "srcid": "5353",
            "all": "1",
            "pointType": "string",
            "group": "quotation_index_minute",
            "query": "000001",
            "code": "000001",
            "market_type": "ab",
            "newFormat": "1",
            "name": "上证指数",
            "finClientType": "pc"
        }
        response = self.baidu_session.get(url, params=params, timeout=10, verify=False)
        try:
            if str(response.json()["ResultCode"]) == "0":
                marketData = response.json()["Result"]["newMarketData"]["marketData"][0]["p"]
                if not is_return:
                    marketData = marketData.split(";")[-30:]
                else:
                    marketData = marketData.split(";")[-15:]
                marketData = [x.split(",")[1:] for x in marketData]
                if marketData:
                    result = []
                    for i in marketData:
                        if not is_return:
                            if "+" in i[2]:
                                i[1] = "\033[1;31m" + i[1]
                            else:
                                i[1] = "\033[1;32m" + i[1]
                        i[3] = i[3] + "%"
                        try:
                            i[4] = str(round(float(float(i[4]) / 10000), 2)) + "万手"
                            i[5] = str(round(float(float(i[5]) / 10000 / 10000), 2)) + "亿"
                        except:
                            pass
                        result.append(i[:-2])
                    if is_return:
                        return result
                    logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 近 30 分钟上证指数:")
                    for line_msg in format_table_msg([
                        [
                            "时间", "指数", "涨跌额", "涨跌幅", "成交量", "成交额"
                        ],
                        *result
                    ]).split("\n"):
                        logger.info(line_msg)
        except Exception as e:
            logger.error(f"获取上证指数信息失败: {e}")
    
    def A_html(self):
        result = self.A(True)
        return get_table_html(
            ["时间", "指数", "涨跌额", "涨跌幅", "成交量", "成交额"],
            result
        )
    
    def seven_A(self, is_return=False):
        url = "https://finance.pae.baidu.com/sapi/v1/metrictrend"
        params = {
            "financeType": "index",
            "market": "ab",
            "code": "000001",
            "targetType": "market",
            "metric": "amount",
            "finClientType": "pc"
        }
        try:
            response = self.baidu_session.get(url, params=params, timeout=10, verify=False)
            if not response.content:
                logger.warning("获取成交量数据失败：返回空响应")
                return [] if is_return else None
            response_data = response.json()
            if str(response_data.get("ResultCode", "")) == "0":
                trend = response_data["Result"]["trend"]
                result = []
                today = datetime.datetime.now()
                dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(8)]
                for i in dates:
                    total = trend[0]
                    ss = trend[1]
                    sz = trend[2]
                    bj = trend[3]
                    total_data = [x for x in total["content"] if x["marketDate"] == i]
                    ss_data = [x for x in ss["content"] if x["marketDate"] == i]
                    sz_data = [x for x in sz["content"] if x["marketDate"] == i]
                    bj_data = [x for x in bj["content"] if x["marketDate"] == i]
                    if total_data and ss_data and sz_data and bj_data:
                        total_amount = total_data[0]["data"]["amount"] + "亿"
                        ss_amount = ss_data[0]["data"]["amount"] + "亿"
                        sz_amount = sz_data[0]["data"]["amount"] + "亿"
                        bj_amount = bj_data[0]["data"]["amount"] + "亿"
                        result.append([
                            i, total_amount, ss_amount, sz_amount, bj_amount
                        ])

                if is_return:
                    return result
                if result:
                    logger.critical(f"{time.strftime('%Y-%m-%d %H:%M')} 近 7 日成交量:")
                    for line_msg in format_table_msg([
                        [
                            "日期", "总成交额", "上交所", "深交所", "北交所"
                        ],
                        *result
                    ]).split("\n"):
                        logger.info(line_msg)
        except Exception as e:
            logger.warning(f"获取成交量数据失败: {str(e)}")
            return [] if is_return else None
    
    def seven_A_html(self):
        result = self.seven_A(True)
        return get_table_html(
            ["日期", "总成交额", "上交所", "深交所", "北交所"],
            result,
            [1, 2, 3, 4]
        )
