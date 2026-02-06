#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import json
import time

"""
测试天天基金网历史净值接口
基金代码: 025209
"""

def get_fund_history_nav(fund_code, start_date, end_date):
    """
    获取基金历史净值数据
    :param fund_code: 基金代码
    :param start_date: 开始日期，格式：YYYY-MM-DD
    :param end_date: 结束日期，格式：YYYY-MM-DD
    :return: 历史净值数据列表
    """
    # 先检查基金是否存在（使用实时估值接口）
    try:
        check_url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        check_response = requests.get(check_url, timeout=5, verify=False)
        if check_response.status_code == 200:
            check_content = check_response.text
            if "jsonpgz(" in check_content:
                print(f"基金 {fund_code} 存在")
            else:
                print(f"基金 {fund_code} 不存在或接口返回异常")
                return []
        else:
            print(f"基金 {fund_code} 不存在或接口返回异常")
            return []
    except Exception as e:
        print(f"检查基金存在性失败: {e}")
    
    # 天天基金网历史净值接口
    url = f"http://fund.eastmoney.com/f10/F10DataApi.aspx"
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
    
    print(f"请求历史净值接口: {url}")
    print(f"参数: {params}")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"响应内容长度: {len(content)}")
            
            # 打印前500个字符，查看响应结构
            print(f"响应内容前500字符: {content[:500]}...")
            
            # 使用更通用的方法解析HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找所有表格
            tables = soup.find_all('table')
            print(f"找到 {len(tables)} 个表格")
            
            history_data = []
            for table in tables:
                # 查找表头
                headers = table.find_all('th')
                if len(headers) >= 4:
                    # 检查表头是否包含净值相关字段
                    header_texts = [th.get_text(strip=True) for th in headers]
                    if ('日期' in header_texts or '净值日期' in header_texts) and '单位净值' in header_texts:
                        print(f"找到净值表格，表头: {header_texts}")
                        
                        # 提取行数据
                        rows = table.find_all('tr')
                        for i, row in enumerate(rows):
                            if i == 0:  # 跳过表头
                                continue
                            
                            # 提取列数据
                            cols = row.find_all('td')
                            if len(cols) >= 4:
                                date = cols[0].get_text(strip=True)
                                unit_nav = cols[1].get_text(strip=True)
                                cumulative_nav = cols[2].get_text(strip=True)
                                daily_growth = cols[3].get_text(strip=True)
                                
                                history_data.append({
                                    "日期": date,
                                    "单位净值": unit_nav,
                                    "累计净值": cumulative_nav,
                                    "日涨跌幅": daily_growth
                                })
                        
                        if history_data:
                            return history_data
            
            # 如果没有找到表格，尝试使用正则表达式
            import re
            # 提取所有<tr>标签
            row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL)
            rows = row_pattern.findall(content)
            
            for i, row in enumerate(rows):
                # 提取列数据
                col_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)
                cols = col_pattern.findall(row)
                
                if len(cols) >= 4:
                    # 清理数据
                    date = re.sub(r'\\s+', '', cols[0])
                    unit_nav = re.sub(r'\\s+', '', cols[1])
                    cumulative_nav = re.sub(r'\\s+', '', cols[2])
                    daily_growth = re.sub(r'\\s+', '', cols[3])
                    
                    # 检查是否是日期格式
                    if re.match(r'\\d{4}-\\d{2}-\\d{2}', date):
                        history_data.append({
                            "日期": date,
                            "单位净值": unit_nav,
                            "累计净值": cumulative_nav,
                            "日涨跌幅": daily_growth
                        })
            
            if history_data:
                return history_data
            else:
                print("未找到历史净值数据")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"获取历史净值失败: {e}")
        import traceback
        traceback.print_exc()
    
    return []

def main():
    """
    主函数
    """
    fund_code = "025209"
    # 获取最近一个月的历史净值
    end_date = time.strftime("%Y-%m-%d")
    import datetime
    start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    
    print(f"开始测试基金 {fund_code} 的历史净值接口...")
    print(f"时间范围: {start_date} 至 {end_date}")
    
    # 获取历史净值数据
    history_data = get_fund_history_nav(fund_code, start_date, end_date)
    
    if history_data:
        print(f"\n成功获取 {len(history_data)} 条历史净值数据:")
        print("=" * 80)
        print(f"{'日期':<12} {'单位净值':<10} {'累计净值':<10} {'日涨跌幅':<8}")
        print("-" * 80)
        
        # 打印前10条数据
        for i, item in enumerate(history_data[:10]):
            print(f"{item['日期']:<12} {item['单位净值']:<10} {item['累计净值']:<10} {item['日涨跌幅']:<8}")
        
        if len(history_data) > 10:
            print(f"... 还有 {len(history_data) - 10} 条数据未显示")
        print("=" * 80)
    else:
        print("未获取到历史净值数据")

if __name__ == "__main__":
    main()
