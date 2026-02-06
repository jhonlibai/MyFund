# -*- coding: UTF-8 -*-

import re
import threading
from typing import Dict, List, Any
import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings()

class FundService:
    """基金数据服务"""
    
    def __init__(self):
        self.session = requests.Session()
        self._csrf = ""
        self.init()
    
    def init(self):
        """初始化会话"""
        res = self.session.get("https://www.fund123.cn/fund", headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }, timeout=10, verify=False)
        self._csrf = re.findall('"csrf":"(.*?)"', res.text)[0]
    
    def get_fund_data(self, fund_code: str) -> Dict[str, Any]:
        """获取单个基金数据"""
        try:
            # 先使用天天基金网的API获取实时估值数据
            forecast_growth = "N/A"
            now_time = "N/A"
            day_of_growth = "0.0%"
            net_value_date = "00-00"
            current_net_value = 0.0
            fund_name = "N/A"
            consecutive_count = 1
            consecutive_growth = "0.0%"
            monthly_growth_day = 0
            monthly_growth_day_count = 0
            monthly_growth_rate = "0.0%"
            
            try:
                # 使用天天基金网的API获取实时估值
                url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
                print(f"请求天天基金网API: {url}")
                response = self.session.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "Referer": "http://fund.eastmoney.com/"
                }, timeout=10, verify=False)
                print(f"响应状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                
                # 解析响应数据
                if response.status_code == 200:
                    # 去除回调函数包装
                    content = response.text
                    print(f"去除包装前的内容: {content}")
                    # 更宽松的格式检查
                    if 'jsonpgz(' in content:
                        # 提取JSON部分
                        start_idx = content.find('jsonpgz(') + 8
                        end_idx = content.rfind(')')
                        if start_idx < end_idx:
                            content = content[start_idx:end_idx]
                            print(f"去除包装后的内容: {content}")
                            import json
                            try:
                                api_data = json.loads(content)
                                print(f"天天基金网API响应: {api_data}")
                                
                                # 提取估值数据
                                forecast_growth = api_data.get('gszzl', 'N/A')  # 实时估值涨跌幅
                                now_time = api_data.get('gztime', 'N/A').split(' ')[1] if 'gztime' in api_data else 'N/A'
                                net_value_date = api_data.get('jzrq', '00-00').replace('-', '/')[5:]
                                current_net_value = float(api_data.get('dwjz', '0.0'))
                                fund_name = api_data.get('name', 'N/A')
                                
                                # 计算实际日涨幅（使用历史净值数据）
                                day_of_growth = "0.0%"
                                try:
                                    # 获取历史净值数据
                                    history_data = self.get_fund_history_nav(api_data.get('fundcode'), start_date=api_data.get('jzrq'), end_date=api_data.get('jzrq'))
                                    if history_data and len(history_data) > 0:
                                        # 获取最新的历史数据
                                        latest_history = history_data[0]
                                        day_of_growth = latest_history.get('daily_growth', '0.0%')
                                except Exception as e:
                                    print(f"获取历史净值数据失败: {e}")
                                
                                # 确保格式正确
                                if forecast_growth != 'N/A':
                                    forecast_growth = f"{forecast_growth}%"
                                if day_of_growth == 'N/A':
                                    day_of_growth = "0.0%"
                                print(f"解析后的数据: forecast_growth={forecast_growth}, now_time={now_time}, day_of_growth={day_of_growth}, net_value_date={net_value_date}, current_net_value={current_net_value}, fund_name={fund_name}")
                            except Exception as json_error:
                                print(f"JSON解析失败: {json_error}")
                        else:
                            print(f"响应内容格式不正确，无法提取JSON部分")
                    else:
                        print(f"响应内容格式不正确，不是jsonpgz格式")
                else:
                    print(f"响应状态码不正确: {response.status_code}")
            except Exception as e:
                print(f"获取实时估值失败: {e}")
                import traceback
                traceback.print_exc()
            
            # 构建返回数据
            fund_data = {
                "fund_code": fund_code,
                "fund_name": fund_name,
                "day_of_growth": day_of_growth,
                "net_value_date": net_value_date,
                "current_net_value": current_net_value,
                "forecast_growth": forecast_growth,
                "now_time": now_time,
                "consecutive_count": consecutive_count,
                "consecutive_growth": consecutive_growth,
                "monthly_growth_day": monthly_growth_day,
                "monthly_growth_day_count": monthly_growth_day_count,
                "monthly_growth_rate": monthly_growth_rate
            }
            
            print(f"返回的fund_data: {fund_data}")
            return fund_data
        except Exception as e:
            print(f"获取基金数据失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                "fund_code": fund_code,
                "error": str(e)
            }
    
    def get_fund_forecast_growth(self, fund_code: str) -> str:
        """获取基金实时估值涨跌幅"""
        try:
            url = "https://www.fund123.cn/api/fund/queryFundEstimateIntraday"
            params = {"_csrf": self._csrf}
            today = datetime.now().strftime("%Y-%m-%d")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            data = {
                "startTime": today,
                "endTime": tomorrow,
                "limit": 200,
                "productId": fund_code,  # 注意：这里可能需要基金的productId
                "format": True,
                "source": "WEALTHBFFWEB"
            }
            response = self.session.post(url, headers={
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Origin": "https://www.fund123.cn",
                "Referer": "https://www.fund123.cn/fund",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "X-API-Key": "foobar",
                "accept": "json"
            }, params=params, json=data, timeout=10, verify=False)
            
            if response.json()["success"] and response.json()["list"]:
                fund_info = response.json()["list"][-1]
                forecast_growth = str(round(float(fund_info["forecastGrowth"]) * 100, 2)) + "%"
                return forecast_growth
            return "N/A"
        except Exception as e:
            print(f"获取基金估值失败: {e}")
            return "N/A"
    
    def get_multiple_funds_data(self, fund_codes: List[str]) -> List[Dict[str, Any]]:
        """批量获取多个基金数据"""
        results = []
        threads = []
        
        def fetch_fund_data(fund_code):
            data = self.get_fund_data(fund_code)
            results.append(data)
        
        for fund_code in fund_codes:
            t = threading.Thread(target=fetch_fund_data, args=(fund_code,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        return results
    
    def get_fund_history_nav(self, fund_code: str, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """
        获取基金历史净值数据
        :param fund_code: 基金代码
        :param start_date: 开始日期，格式：YYYY-MM-DD，默认为30天前
        :param end_date: 结束日期，格式：YYYY-MM-DD，默认为今天
        :return: 历史净值数据列表
        """
        # 设置默认日期范围
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        print(f"获取基金 {fund_code} 的历史净值数据，时间范围: {start_date} 至 {end_date}")
        
        # 天天基金网历史净值接口
        url = "http://fund.eastmoney.com/f10/F10DataApi.aspx"
        params = {
            "type": "lsjz",
            "code": fund_code,
            "page": "1",
            "per": "40",
            "sdate": start_date,
            "edate": end_date
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": f"http://fund.eastmoney.com/{fund_code}.html"
        }
        
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=10, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"响应内容长度: {len(content)}")
                
                # 解析HTML内容
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # 查找净值表格
                tables = soup.find_all('table')
                history_data = []
                
                for table in tables:
                    headers = table.find_all('th')
                    if len(headers) >= 4:
                        header_texts = [th.get_text(strip=True) for th in headers]
                        if ('日期' in header_texts or '净值日期' in header_texts) and '单位净值' in header_texts:
                            print(f"找到净值表格，表头: {header_texts}")
                            
                            # 提取行数据
                            rows = table.find_all('tr')
                            for i, row in enumerate(rows):
                                if i == 0:  # 跳过表头
                                    continue
                                
                                cols = row.find_all('td')
                                if len(cols) >= 4:
                                    date = cols[0].get_text(strip=True)
                                    unit_nav = cols[1].get_text(strip=True)
                                    cumulative_nav = cols[2].get_text(strip=True)
                                    daily_growth = cols[3].get_text(strip=True)
                                    
                                    history_data.append({
                                        "date": date,
                                        "unit_nav": unit_nav,
                                        "cumulative_nav": cumulative_nav,
                                        "daily_growth": daily_growth
                                    })
                            
                            if history_data:
                                print(f"成功获取 {len(history_data)} 条历史净值数据")
                                return history_data
                
                print("未找到历史净值表格数据")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"获取历史净值失败: {e}")
            import traceback
            traceback.print_exc()
        
        return []
