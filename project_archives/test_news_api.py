import requests
import json

# 测试百度财经快讯API
def test_news_api():
    print("测试百度财经快讯API...")
    
    # 百度财经快讯接口
    count = 10
    url = f"https://finance.pae.baidu.com/selfselect/expressnews?rn={count}&pn=0&tag=A股&finClientType=pc"
    
    # 添加请求头，模拟浏览器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.encoding = response.apparent_encoding
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应编码: {response.encoding}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"ResultCode: {data.get('ResultCode')}")
            
            if data.get('ResultCode') == '0':
                kx_list = data.get('Result', {}).get('content', {}).get('list', [])
                print(f"获取到 {len(kx_list)} 条快讯")
                
                for i, item in enumerate(kx_list[:5]):  # 只显示前5条
                    print(f"\n第 {i+1} 条:")
                    print(f"时间: {item.get('time')}")
                    print(f"标题: {item.get('title')}")
                    print(f"内容: {item.get('content')}")
    except Exception as e:
        print(f"错误: {e}")

# 测试我们的后端API
def test_backend_api():
    print("\n\n测试后端API...")
    
    url = "http://localhost:8000/api/market/news"
    
    try:
        response = requests.get(url, timeout=10)
        response.encoding = response.apparent_encoding
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应编码: {response.encoding}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"获取到 {len(data)} 条新闻")
            
            for i, item in enumerate(data[:5]):  # 只显示前5条
                print(f"\n第 {i+1} 条:")
                print(f"时间: {item.get('time')}")
                print(f"内容: {item.get('content')}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_news_api()
    test_backend_api()
