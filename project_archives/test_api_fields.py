import requests
import json
import re
from bs4 import BeautifulSoup
import sys

# 禁用SSL警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TianTianFundAPITester:
    """天天基金网API测试器"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "http://fund.eastmoney.com/"
        }
    
    def test_real_time_valuation(self, fund_code="000001"):
        """测试实时估值接口"""
        print("\n=== 测试实时估值接口 ===")
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        print(f"请求URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"响应内容长度: {len(content)}")
                print(f"响应内容前200字符: {content[:200]}...")
                
                # 去除JSONP包装
                try:
                    # 尝试提取JSON部分
                    if 'jsonpgz(' in content:
                        # 找到jsonpgz(的位置
                        start_idx = content.find('jsonpgz(') + 8
                        # 找到最后一个)的位置
                        end_idx = content.rfind(')')
                        if start_idx < end_idx:
                            json_content = content[start_idx:end_idx]
                            try:
                                data = json.loads(json_content)
                                print("\n解析后的JSON数据:")
                                print(f"字段数量: {len(data.keys())}")
                                print("字段列表:")
                                for key, value in data.items():
                                    print(f"  - {key}: {value} (类型: {type(value).__name__})")
                                return data
                            except json.JSONDecodeError as e:
                                print(f"JSON解析失败: {e}")
                                print(f"尝试解析的内容: {json_content}")
                    print("响应内容可能不是标准JSONP格式")
                    print(f"完整响应内容: {content}")
                except Exception as e:
                    print(f"处理响应内容时出错: {e}")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"测试失败: {e}")
        return None
    
    def test_historical_net_value(self, fund_code="000001", start_date="2024-01-01", end_date="2024-01-10"):
        """测试历史净值接口"""
        print("\n=== 测试历史净值接口 ===")
        url = f"http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={fund_code}&sdate={start_date}&edate={end_date}"
        print(f"请求URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"响应内容长度: {len(content)}")
                
                # 解析HTML
                soup = BeautifulSoup(content, "html.parser")
                table = soup.find("table", class_="w782")
                
                if table:
                    print("\n找到历史净值表格:")
                    # 提取表头
                    headers = [th.text.strip() for th in table.find_all("th")]
                    print(f"表头字段: {headers}")
                    
                    # 提取数据行
                    rows = []
                    for tr in table.find_all("tr")[1:]:
                        cells = [td.text.strip() for td in tr.find_all("td")]
                        if cells:
                            rows.append(dict(zip(headers, cells)))
                    
                    print(f"数据行数: {len(rows)}")
                    if rows:
                        print("前2条数据示例:")
                        for i, row in enumerate(rows[:2]):
                            print(f"  第{i+1}条: {row}")
                    return rows
                else:
                    print("未找到历史净值表格")
                    print(f"响应内容前300字符: {content[:300]}...")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"测试失败: {e}")
        return None
    
    def test_basic_info(self, fund_code="000001"):
        """测试基本信息接口"""
        print("\n=== 测试基本信息接口 ===")
        url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
        print(f"请求URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"响应内容长度: {len(content)}")
                print(f"响应内容前300字符: {content[:300]}...")
                
                # 提取关键信息
                info = {}
                
                # 基金名称
                fund_name_match = re.search(r'var fS_name = "(.*?)";', content)
                if fund_name_match:
                    info["fund_name"] = fund_name_match.group(1)
                else:
                    fund_name_match = re.search(r'var fund_name = "(.*?)";', content)
                    if fund_name_match:
                        info["fund_name"] = fund_name_match.group(1)
                
                # 基金代码
                fund_code_match = re.search(r'var fS_code = "(.*?)";', content)
                if fund_code_match:
                    info["fund_code"] = fund_code_match.group(1)
                
                # 基金类型
                fund_type_match = re.search(r'var fund_type = "(.*?)";', content)
                if fund_type_match:
                    info["fund_type"] = fund_type_match.group(1)
                
                # 成立日期
                establish_date_match = re.search(r'var establish_date = "(.*?)";', content)
                if establish_date_match:
                    info["establish_date"] = establish_date_match.group(1)
                
                # 基金经理
                fund_manager_match = re.search(r'var fund_manager = "(.*?)";', content)
                if fund_manager_match:
                    info["fund_manager"] = fund_manager_match.group(1)
                
                # 基金公司
                fund_company_match = re.search(r'var fund_company = "(.*?)";', content)
                if fund_company_match:
                    info["fund_company"] = fund_company_match.group(1)
                
                # 费率相关
                source_rate_match = re.search(r'var fund_sourceRate="(.*?)";', content)
                if source_rate_match:
                    info["source_rate"] = source_rate_match.group(1)
                
                rate_match = re.search(r'var fund_Rate="(.*?)";', content)
                if rate_match:
                    info["rate"] = rate_match.group(1)
                
                # 最小申购金额
                min_sg_match = re.search(r'var fund_minsg="(.*?)";', content)
                if min_sg_match:
                    info["min_sg"] = min_sg_match.group(1)
                
                print("\n提取的基本信息:")
                if info:
                    for key, value in info.items():
                        print(f"  - {key}: {value}")
                else:
                    print("  未提取到任何信息，可能变量名与预期不同")
                
                # 查找涨跌幅相关数据
                print("\n查找涨跌幅相关数据:")
                growth_patterns = [
                    ("week", r'var Data_week = \[(.*?)\];'),
                    ("month", r'var Data_month = \[(.*?)\];'),
                    ("quarter", r'var Data_quarter = \[(.*?)\];'),
                    ("halfyear", r'var Data_halfyear = \[(.*?)\];'),
                    ("year", r'var Data_year = \[(.*?)\];'),
                    ("30days", r'var Data_30days = \[(.*?)\];')
                ]
                
                found_growth_data = False
                for period, pattern in growth_patterns:
                    match = re.search(pattern, content)
                    if match:
                        print(f"  Data_{period}: {match.group(1)}")
                        found_growth_data = True
                
                if not found_growth_data:
                    print("  未找到涨跌幅相关数据字段")
                
                # 打印响应内容的前500字符，以便分析实际格式
                print("\n响应内容前500字符:")
                print(content[:500] + "...")
                
                return info
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"测试失败: {e}")
        return None
    
    def test_fund_company_list(self):
        """测试基金公司列表接口"""
        print("\n=== 测试基金公司列表接口 ===")
        url = "http://fund.eastmoney.com/Data/FundRankList.aspx?t=1&pi=1&pn=50"
        print(f"请求URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"响应内容长度: {len(content)}")
                print(f"响应内容前300字符: {content[:300]}...")
                
                # 解析HTML
                soup = BeautifulSoup(content, "html.parser")
                table = soup.find("table")
                
                if table:
                    print("\n找到基金公司表格:")
                    # 提取表头
                    headers = [th.text.strip() for th in table.find_all("th")]
                    print(f"表头字段: {headers}")
                    
                    # 提取数据行
                    rows = []
                    for tr in table.find_all("tr")[1:]:
                        cells = [td.text.strip() for td in tr.find_all("td")]
                        if cells:
                            rows.append(cells)
                    
                    print(f"数据行数: {len(rows)}")
                    if rows:
                        print("前3条数据示例:")
                        for i, row in enumerate(rows[:3]):
                            print(f"  第{i+1}条: {row}")
                    return rows
                else:
                    print("未找到基金公司表格")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"测试失败: {e}")
        return None
    
    def test_fund_ranking(self, fund_type="1"):
        """测试基金排行接口"""
        print("\n=== 测试基金排行接口 ===")
        url = f"http://fund.eastmoney.com/Data/FundRankList.aspx?t={fund_type}&pi=1&pn=50"
        print(f"请求URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"响应内容长度: {len(content)}")
                print(f"响应内容前300字符: {content[:300]}...")
                
                # 解析HTML
                soup = BeautifulSoup(content, "html.parser")
                table = soup.find("table")
                
                if table:
                    print("\n找到基金排行表格:")
                    # 提取表头
                    headers = [th.text.strip() for th in table.find_all("th")]
                    print(f"表头字段: {headers}")
                    
                    # 提取数据行
                    rows = []
                    for tr in table.find_all("tr")[1:]:
                        cells = [td.text.strip() for td in tr.find_all("td")]
                        if cells:
                            rows.append(cells)
                    
                    print(f"数据行数: {len(rows)}")
                    if rows:
                        print("前3条数据示例:")
                        for i, row in enumerate(rows[:3]):
                            print(f"  第{i+1}条: {row}")
                    return rows
                else:
                    print("未找到基金排行表格")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"测试失败: {e}")
        return None
    
    def test_fund_search(self, keyword="华夏"):
        """测试基金搜索接口"""
        print("\n=== 测试基金搜索接口 ===")
        url = f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchSuggest?key={keyword}"
        print(f"请求URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"响应内容长度: {len(content)}")
                
                try:
                    data = json.loads(content)
                    print("\n解析后的JSON数据:")
                    print(f"数据结构: {list(data.keys())}")
                    
                    if "Data" in data:
                        print(f"Data字段长度: {len(data['Data'])}")
                        if data['Data']:
                            print("前3条搜索结果:")
                            for i, item in enumerate(data['Data'][:3]):
                                print(f"  第{i+1}条: {item}")
                    
                    return data
                except json.JSONDecodeError as e:
                    print(f"JSON解析失败: {e}")
                    print(f"响应内容: {content}")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"测试失败: {e}")
        return None
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=====================================")
        print("天天基金网API接口测试与字段分析")
        print("=====================================")
        
        # 测试实时估值接口
        real_time_data = self.test_real_time_valuation()
        
        # 测试历史净值接口
        historical_data = self.test_historical_net_value()
        
        # 测试基本信息接口
        basic_info_data = self.test_basic_info()
        
        # 测试基金公司列表接口
        company_list_data = self.test_fund_company_list()
        
        # 测试基金排行接口
        ranking_data = self.test_fund_ranking()
        
        # 测试基金搜索接口
        search_data = self.test_fund_search()
        
        print("\n=====================================")
        print("测试完成！")
        print("=====================================")
        
        # 生成分析报告
        self.generate_report({
            "real_time_valuation": real_time_data,
            "historical_net_value": historical_data,
            "basic_info": basic_info_data,
            "fund_company_list": company_list_data,
            "fund_ranking": ranking_data,
            "fund_search": search_data
        })
    
    def generate_report(self, test_results):
        """生成测试报告"""
        print("\n=== API接口字段分析报告 ===")
        
        # 实时估值接口分析
        if test_results["real_time_valuation"]:
            print("\n1. 实时估值接口字段分析:")
            data = test_results["real_time_valuation"]
            print(f"   字段数量: {len(data.keys())}")
            print("   字段详情:")
            field_descriptions = {
                "fundcode": "基金代码",
                "name": "基金名称",
                "jzrq": "净值日期",
                "dwjz": "单位净值",
                "gsz": "估值",
                "gszzl": "估值涨跌幅（百分比）",
                "gztime": "估值时间"
            }
            for field, value in data.items():
                desc = field_descriptions.get(field, "未知字段")
                print(f"   - {field}: {desc} (值: {value}, 类型: {type(value).__name__})")
        
        # 基本信息接口分析
        if test_results["basic_info"]:
            print("\n2. 基本信息接口字段分析:")
            data = test_results["basic_info"]
            print(f"   提取字段数量: {len(data.keys())}")
            print("   关键字段:")
            for field, value in data.items():
                print(f"   - {field}: {value}")
            print("   注意: 该接口返回的是JavaScript代码，包含大量字段，")
            print("         本测试仅提取了部分关键字段。")
        
        # 基金搜索接口分析
        if test_results["fund_search"]:
            print("\n3. 基金搜索接口字段分析:")
            data = test_results["fund_search"]
            print(f"   顶层字段: {list(data.keys())}")
            if "Data" in data and data["Data"]:
                print(f"   搜索结果数量: {len(data['Data'])}")
                if data["Data"]:
                    first_item = data["Data"][0]
                    print(f"   每条结果字段: {list(first_item.keys())}")
        
        # 历史净值接口分析
        if test_results["historical_net_value"]:
            print("\n4. 历史净值接口分析:")
            data = test_results["historical_net_value"]
            print(f"   返回数据行数: {len(data)}")
            if data:
                first_row = data[0]
                print(f"   每行字段: {list(first_row.keys())}")
        
        print("\n=== 总结 ===")
        print("1. 实时估值接口: 返回基金的实时估值数据，包含基金代码、名称、净值、估值、涨跌幅等字段")
        print("2. 历史净值接口: 返回基金的历史净值数据，以表格形式呈现，包含日期、单位净值、累计净值、日涨跌幅等字段")
        print("3. 基本信息接口: 返回基金的详细基本信息，包含基金名称、类型、成立日期、基金经理、公司等信息")
        print("4. 基金公司列表接口: 返回基金公司列表数据，以表格形式呈现")
        print("5. 基金排行接口: 返回基金排行榜数据，以表格形式呈现")
        print("6. 基金搜索接口: 返回基金搜索结果，包含基金代码、名称等信息")
        print("\n注意: 部分接口返回HTML格式数据，需要使用BeautifulSoup等库进行解析。")

if __name__ == "__main__":
    tester = TianTianFundAPITester()
    tester.run_all_tests()
