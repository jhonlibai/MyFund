#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
百度财经API调试脚本
用于调试market_fetcher.py中的kx方法
"""

import requests
import json
import time
import datetime
from market_fetcher import MarketFetcher

class DebugMarketFetcher(MarketFetcher):
    """扩展MarketFetcher类，添加详细的调试日志"""
    
    def kx(self, is_return=False, count=10):
        """重写kx方法，添加详细的调试信息"""
        url = f"https://finance.pae.baidu.com/selfselect/expressnews?rn={count}&pn=0&tag=A股&finClientType=pc"
        kx_list = []
        
        print(f"\n{'='*60}")
        print(f"开始请求百度财经API")
        print(f"请求URL: {url}")
        print(f"请求头: {json.dumps(dict(self.baidu_session.headers), indent=2, ensure_ascii=False)}")
        
        try:
            start_time = time.time()
            response = self.baidu_session.get(url, timeout=10, verify=False)
            end_time = time.time()
            
            print(f"\n响应状态码: {response.status_code}")
            print(f"响应时间: {end_time - start_time:.2f}秒")
            print(f"响应编码: {response.encoding}")
            print(f"响应头: {json.dumps(dict(response.headers), indent=2, ensure_ascii=False)}")
            
            # 打印完整的响应内容
            print(f"\n响应内容: {response.text}")
            
            # 尝试解析JSON
            try:
                data = response.json()
                print(f"\n解析后的JSON数据:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                if data.get("ResultCode") == "0":
                    kx_list = data.get("Result", {}).get("content", {}).get("list", [])
                    print(f"\n获取到 {len(kx_list)} 条快讯")
                    
                    # 打印第一条快讯的详细信息
                    if kx_list:
                        print(f"\n第一条快讯详细信息:")
                        print(json.dumps(kx_list[0], indent=2, ensure_ascii=False))
                else:
                    print(f"\nAPI错误: {data.get('ResultMsg', '未知错误')}")
            except json.JSONDecodeError as e:
                print(f"\nJSON解析错误: {e}")
                print(f"响应内容长度: {len(response.text)}")
                print(f"响应内容前500字符: {response.text[:500]}...")
        except Exception as e:
            print(f"\n请求错误: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n{'='*60}")
        
        if is_return:
            return kx_list

        # 后续代码保持不变
        if kx_list:
            print(f"{time.strftime('%Y-%m-%d %H:%M')} 7*24 快讯:")
            for i, v in enumerate(kx_list):
                evaluate = v.get("evaluate", "")
                if evaluate == "利好":
                    pre = ""
                elif evaluate == "利空":
                    pre = ""
                else:
                    pre = ""
                title = v.get("title", v["content"]["items"][0]["data"])
                publish_time = v["publish_time"]
                publish_time = datetime.datetime.fromtimestamp(int(publish_time)).strftime("%Y-%m-%d %H:%M:%S")
                entity = v.get("entity", [])
                entity = ", ".join([f"{x['code'].strip()}-{x['name'].strip()} {x['ratio'].strip()}" for x in entity])
                print(f"{pre}{i + 1}. {publish_time} {title}.")
                if entity:
                    print(f"影响股票: {entity}.")

def test_baidu_api():
    """测试百度财经API"""
    print("=== 百度财经API调试测试 ===")
    
    # 创建会话
    session = requests.Session()
    session.verify = False
    
    # 测试1: 使用默认请求头
    print("\n=== 测试1: 使用默认请求头 ===")
    fetcher1 = DebugMarketFetcher(session)
    result1 = fetcher1.kx(is_return=True, count=5)
    print(f"测试1结果: 获取到 {len(result1)} 条快讯")
    
    # 测试2: 使用不同的请求头
    print("\n=== 测试2: 使用修改后的请求头 ===")
    session2 = requests.Session()
    session2.verify = False
    # 添加更完整的请求头
    session2.headers = {
        "accept": "application/vnd.finance-web.v1+json",
        "accept-language": "zh-CN,zh;q=0.9",
        "connection": "keep-alive",
        "origin": "https://finance.baidu.com",
        "referer": "https://finance.baidu.com/",
        "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    
    fetcher2 = DebugMarketFetcher(session2)
    result2 = fetcher2.kx(is_return=True, count=5)
    print(f"测试2结果: 获取到 {len(result2)} 条快讯")
    
    # 测试3: 直接请求，不使用MarketFetcher
    print("\n=== 测试3: 直接请求API ===")
    test_direct_request()

def test_direct_request():
    """直接测试API请求"""
    url = "https://finance.pae.baidu.com/selfselect/expressnews?rn=5&pn=0&tag=A股&finClientType=pc"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Referer": "https://finance.baidu.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }
    
    print(f"直接请求URL: {url}")
    print(f"请求头: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\nJSON数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print("\n无法解析JSON")
    except Exception as e:
        print(f"\n错误: {e}")

if __name__ == "__main__":
    test_baidu_api()
