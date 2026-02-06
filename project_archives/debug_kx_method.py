#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
直接复用market_fetcher.py中的kx方法进行调试
"""

import requests
import json
import time
import datetime

class DebugKx:
    """直接复用kx方法的调试类"""
    
    def __init__(self):
        # 创建会话
        self.baidu_session = requests.Session()
        self.baidu_session.verify = False
        # 设置请求头
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
    
    def kx(self, is_return=False, count=10):
        """直接复用的kx方法，添加详细调试信息"""
        # 直接复制market_fetcher.py中的代码
        url = f"https://finance.pae.baidu.com/selfselect/expressnews?rn={count}&pn=0&tag=A股&finClientType=pc"
        kx_list = []
        
        print(f"\n{'='*80}")
        print(f"原始kx方法调试")
        print(f"URL: {url}")
        print(f"请求头: {json.dumps(dict(self.baidu_session.headers), indent=2, ensure_ascii=False)}")
        
        try:
            response = self.baidu_session.get(url, timeout=10, verify=False)
            print(f"\n响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.json()["ResultCode"] == "0":
                kx_list = response.json()["Result"]["content"]["list"]
                print(f"\n成功获取到 {len(kx_list)} 条快讯")
                
                # 详细展示每条快讯
                for i, v in enumerate(kx_list):
                    print(f"\n第 {i+1} 条快讯:")
                    print(f"完整数据: {json.dumps(v, indent=2, ensure_ascii=False)}")
            else:
                print(f"\nAPI错误: ResultCode = {response.json().get('ResultCode')}")
                print(f"错误信息: {response.json()}")
        except Exception as e:
            print(f"\n异常: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n{'='*80}")
        
        if is_return:
            return kx_list
        
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

def test_kx_method():
    """测试kx方法"""
    print("=== 直接复用kx方法调试 ===")
    
    debug = DebugKx()
    
    # 测试1: 默认参数
    print("\n=== 测试1: 默认参数 (count=10) ===")
    debug.kx(is_return=False, count=10)
    
    # 测试2: 不同的count值
    print("\n=== 测试2: count=5 ===")
    result = debug.kx(is_return=True, count=5)
    print(f"返回结果长度: {len(result)}")

if __name__ == "__main__":
    test_kx_method()
