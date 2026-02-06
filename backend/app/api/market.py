# -*- coding: UTF-8 -*-

from fastapi import APIRouter
from typing import Dict, Any, List
import requests
import json
import random

# 导入curl_cffi
from curl_cffi import requests as curl_requests

router = APIRouter()

class BaiduNewsFetcher:
    """百度财经新闻获取器"""
    
    def __init__(self):
        self.session = None
    
    def get_session(self):
        """获取会话"""
        if not self.session:
            self.session = curl_requests.Session()
            self.session.impersonate = "chrome107"
            # 先访问主页获取cookie
            try:
                self.session.get("https://finance.baidu.com/", timeout=10)
            except Exception as e:
                print(f"访问百度财经主页错误: {e}")
        return self.session
    
    def fetch_news(self, count=10):
        """获取快讯数据"""
        url = f"https://finance.pae.baidu.com/selfselect/expressnews?rn={count}&pn=0&tag=A股&finClientType=pc"
        
        session = self.get_session()
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Referer": "https://finance.baidu.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        
        kx_list = []
        try:
            response = session.get(url, headers=headers, timeout=10)
            print(f"百度财经API响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"百度财经API ResultCode: {data.get('ResultCode')}")
                
                if data.get("ResultCode") == "0":
                    kx_list = data.get("Result", {}).get("content", {}).get("list", [])
                    print(f"获取到 {len(kx_list)} 条快讯")
                else:
                    print(f"百度财经API错误: {data}")
            else:
                print(f"百度财经API请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"百度财经API请求错误: {e}")
        
        return kx_list

# 创建新闻获取器实例
news_fetcher = BaiduNewsFetcher()

BK_MAP = {
    "光模块": "BK000651",
    "F5G": "BK000652",
    "CPO": "BK000641",
    "航天装备": "BK000157",
    "通信设备": "BK000176",
    "PCB": "BK000644",
    "小金属": "BK000051",
    "有色金属": "BK000047",
    "工业金属": "BK000049",
    "卫星互联网": "BK000347",
    "元件": "BK000055",
    "商业航天": "BK000313",
    "黄金股": "BK000292",
    "存储芯片": "BK000642",
    "光通信": "BK000501",
    "算力": "BK000601",
    "脑机接口": "BK000663",
    "军工电子": "BK000161",
    "通信": "BK000174",
    "消费电子": "BK000058",
    "风电设备": "BK000147",
    "家电零部件": "BK000072",
    "稀土永磁": "BK000228",
    "贵金属": "BK000050",
    "可控核聚变": "BK000649",
    "5G": "BK000291",
    "游戏": "BK000387",
    "毫米波": "BK000370",
    "电子": "BK000053",
    "人工智能": "BK000217",
    "通用设备": "BK000151",
    "半导体": "BK000054",
    "电机": "BK000144",
    "光刻胶": "BK000331",
    "液冷": "BK000653",
    "智能穿戴": "BK000248",
    "云计算": "BK000266",
    "专用设备": "BK000152",
    "材料": "BK000195",
    "电子化学品": "BK000059",
    "TMT": "BK000388",
    "锂矿": "BK000645",
    "CRO": "BK000353",
    "工业4.0": "BK000236",
    "科技": "BK000391",
    "第三代半导体": "BK000239",
    "DeepSeek": "BK000561",
    "Web3.0": "BK000326",
    "人形机器人": "BK000581",
    "国防军工": "BK000156",
    "传媒": "BK000166",
    "LED": "BK000393",
    "机械设备": "BK000150",
    "高端装备": "BK000441",
    "AI眼镜": "BK000647",
    "医疗服务": "BK000096",
    "特斯拉": "BK000300",
    "汽车热管理": "BK000251",
    "尾气治理": "BK000346",
    "军民融合": "BK000298",
    "电力设备": "BK000143",
    "智能家居": "BK000247",
    "电池": "BK000148",
    "锂电池": "BK000295",
    "电网设备": "BK000149",
    "IT服务": "BK000164",
    "信创": "BK000299",
    "新能源车": "BK000225",
    "汽车零部件": "BK000061",
    "工程机械": "BK000154",
    "高端制造": "BK000481",
    "低空经济": "BK000521",
    "AI手机": "BK000650",
    "东数西算": "BK000325",
    "工业互联": "BK000392",
    "元宇宙": "BK000305",
    "软件开发": "BK000165",
    "AIGC": "BK000369",
    "影视": "BK000286",
    "计算机": "BK000162",
    "新能源": "BK000226",
    "基础化工": "BK000035",
    "华为": "BK000293",
    "新兴产业": "BK000389",
    "无人驾驶": "BK000279",
    "资源": "BK000386",
    "充电桩": "BK000301",
    "大宗商品": "BK000204",
    "国产软件": "BK000216",
    "自动化设备": "BK000155",
    "化学制药": "BK000091",
    "AI应用": "BK000681",
    "国家安防": "BK000232",
    "一带一路": "BK000254",
    "固态电池": "BK000362",
    "基因测序": "BK000321",
    "国资云": "BK000278",
    "建筑材料": "BK000133",
    "计算机设备": "BK000163",
    "机器人": "BK000234",
    "光伏设备": "BK000146",
    "新消费": "BK000621",
    "精准医疗": "BK000484",
    "在线教育": "BK000220",
    "钢铁": "BK000043",
    "氢能源": "BK000227",
    "创新药": "BK000208",
    "并购重组": "BK000483",
    "农牧主题": "BK000200",
    "碳中和": "BK000482",
    "环保设备": "BK000186",
    "安全主题": "BK000194",
    "轻工制造": "BK000085",
    "超级真菌": "BK000367",
    "储能": "BK000230",
    "保险": "BK000129",
    "社会服务": "BK000114",
    "垃圾分类": "BK000309",
    "教育": "BK000120",
    "航空装备": "BK000158",
    "智能驾驶": "BK000461",
    "超清视频": "BK000307",
    "家居用品": "BK000088",
    "数字孪生": "BK000327",
    "环保": "BK000184",
    "商贸零售": "BK000108",
    "医药生物": "BK000090",
    "数据要素": "BK000602",
    "网络安全": "BK000258",
    "环境治理": "BK000185",
    "汽车": "BK000060",
    "生物疫苗": "BK000280",
    "文娱用品": "BK000089",
    "光学光电子": "BK000056",
    "农林牧渔": "BK000026",
    "纺织服饰": "BK000081",
    "建筑装饰": "BK000137",
    "生物制品": "BK000093",
    "航母": "BK000339",
    "非银金融": "BK000127",
    "养老产业": "BK000256",
    "医疗器械": "BK000095",
    "婴童": "BK000303",
    "国有大型银行": "BK000122",
    "国企改革": "BK000203",
    "通用航空": "BK000264",
    "家用电器": "BK000066",
    "汽车服务": "BK000062",
    "金融": "BK000199",
    "中特估": "BK000421",
    "中字头": "BK000308",
    "养殖业": "BK000032",
    "航海装备": "BK000160",
    "体育": "BK000115",
    "通信服务": "BK000175",
    "银行": "BK000121",
    "可选消费": "BK000198",
    "房地产开发": "BK000106",
    "房地产": "BK000105",
    "绿色电力": "BK000209",
    "石油石化": "BK000180",
    "房地产服务": "BK000107",
    "物流": "BK000101",
    "猪肉": "BK000340",
    "证券": "BK000128",
    "公用事业": "BK000097",
    "煤炭": "BK000177",
    "航空机场": "BK000103",
    "煤炭开采": "BK000178",
    "能源": "BK000197",
    "电力": "BK000098",
    "城商行": "BK000124",
    "交通运输": "BK000100",
    "消费": "BK000390",
    "新零售": "BK000262",
    "股份制银行": "BK000123",
    "中药": "BK000092",
    "食品饮料": "BK000074",
    "白酒": "BK000076"
}

# 创建id到板块名称的映射
id_map = {}
bk_list = list(BK_MAP.keys())
for i in range(len(bk_list)):
    id_map[str(i + 1)] = bk_list[i]

@router.get("/indices", response_model=Dict[str, Any])
async def get_market_indices():
    """获取全球指数"""
    try:
        import datetime
        import time
        
        # 创建百度会话
        session = news_fetcher.get_session()
        
        headers = {
            "accept": "application/vnd.finance-web.v1+json",
            "accept-language": "zh-CN,zh;q=0.9",
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
        
        result = []
        markets = ["asia", "america"]
        for market in markets:
            url = f"https://finance.pae.baidu.com/api/getbanner?market={market}&finClientType=pc"
            try:
                response = session.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("ResultCode") == "0":
                        market_list = data.get("Result", {}).get("list", [])
                        for market_info in market_list:
                            result.append([
                                market_info.get("name"),
                                market_info.get("lastPrice"),
                                market_info.get("ratio")
                            ])
            except Exception as e:
                print(f"获取{market}市场信息失败: {e}")
        
        # 获取创业板指
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
        try:
            response = session.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if str(data.get("ResultCode")) == "0":
                    cur = data.get("Result", {}).get("cur", {})
                    if cur:
                        result.insert(2, [
                            "创业板指",
                            cur.get("price"),
                            cur.get("ratio")
                        ])
        except Exception as e:
            print(f"获取创业板指信息失败: {e}")
        
        # 构建返回数据
        us_indices = {}
        asia_indices = {}
        
        for item in result:
            name, price, ratio = item
            if "道琼斯" in name or "纳斯达克" in name or "标普" in name:
                if "道琼斯" in name:
                    us_indices["Dow Jones"] = price
                elif "纳斯达克" in name:
                    us_indices["Nasdaq"] = price
                elif "标普" in name:
                    us_indices["S&P 500"] = price
            else:
                if "日经" in name:
                    asia_indices["Nikkei"] = price
                elif "恒生" in name:
                    asia_indices["Hang Seng"] = price
                elif "上证指数" in name:
                    asia_indices["Shanghai"] = price
        
        # 如果没有获取到数据，返回模拟数据作为 fallback
        if not us_indices:
            us_indices = {
                "Dow Jones": "49407.66",
                "Nasdaq": "23592.11",
                "S&P 500": "6976.44"
            }
        
        if not asia_indices:
            asia_indices = {
                "Nikkei": "54201.01",
                "Hang Seng": "16897.11",
                "Shanghai": "4012.34"
            }
        
        return {
            "US": us_indices,
            "Asia": asia_indices
        }
    except Exception as e:
        print(f"获取全球指数失败: {e}")
        # 返回模拟数据作为 fallback
        return {
            "US": {
                "Dow Jones": "49407.66",
                "Nasdaq": "23592.11",
                "S&P 500": "6976.44"
            },
            "Asia": {
                "Nikkei": "54201.01",
                "Hang Seng": "16897.11",
                "Shanghai": "4012.34"
            }
        }

@router.get("/gold", response_model=Dict[str, Any])
async def get_gold_price():
    """获取金价"""
    try:
        import datetime
        import time
        import requests
        import json
        import json
        import json
        
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
        
        # 获取中国黄金基础金价
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
        # 确保使用正确的编码解析响应
        response.encoding = response.apparent_encoding
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
        # 确保使用正确的编码解析响应
        response.encoding = response.apparent_encoding
        data2 = json.loads(response.text.replace("var quote_json = ", ""))["data"]
        
        gold_list = []
        history = []
        
        for i in range(len(data)):
            gold = data[i]
            t = gold["time"]
            date = datetime.datetime.fromtimestamp(t / 1000).strftime("%Y-%m-%d")
            price = gold.get("q1", "N/A")
            radio = str(gold.get("q70", "N/A"))
            
            # 添加到历史数据
            history.append({"date": date, "price": str(price)})
            
            radio2 = "N/A"
            gold2 = {}
            if len(data2) > i:
                gold2 = data2[i]
                radio2 = str(gold2.get("q70", "N/A"))
            
            gold_list.append([
                date,
                price,
                gold2.get("q1", "N/A"),
                radio,
                radio2
            ])
        
        # 获取最新价格和变化
        if gold_list:
            latest = gold_list[-1]
            current = str(latest[1])
            change = latest[3]
            
            # 构建返回数据
            return {
                "current": current,
                "change": change,
                "history": history[:5]  # 返回最近5条历史数据
            }
        else:
            # 返回模拟数据作为 fallback
            return {
                "current": "2023.50",
                "change": "-6.53%",
                "history": [
                    {"date": "2026-02-02", "price": "2164.80"},
                    {"date": "2026-02-01", "price": "2180.50"}
                ]
            }
    except Exception as e:
        print(f"获取金价失败: {e}")
        # 返回模拟数据作为 fallback
        return {
            "current": "2023.50",
            "change": "-6.53%",
            "history": [
                {"date": "2026-02-02", "price": "2164.80"},
                {"date": "2026-02-01", "price": "2180.50"}
            ]
        }

@router.get("/real-time-gold", response_model=List[Dict[str, Any]])
async def get_real_time_gold():
    """获取实时贵金属价格"""
    try:
        import datetime
        import time
        import requests
        import json
        
        # 直接复用market_fetcher.py的实现
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
        
        url = "https://api.jijinhao.com/quoteCenter/realTime.htm"
        params = {
            "codes": "JO_71,JO_92233,JO_92232,JO_75",
            "_": str(int(time.time() * 1000))
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
        # 直接使用content并指定编码
        content = response.content
        # 尝试不同的编码方式
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = content.decode('gbk')
            except UnicodeDecodeError:
                text = content.decode('gb2312', errors='ignore')
        # 移除可能的前缀，确保返回的是有效的JSON
        if text.startswith("var quote_json ="):
            text = text.replace("var quote_json = ", "")
        data = json.loads(text)
        
        result = []
        if data:
            # 黄金9999
            if "JO_71" in data:
                data1 = data["JO_71"]
                keys = ["showName", "q63", "q70", "q80", "q1", "q3", "q4", "q2", "time", "unit"]
                gold_data = {}
                for key in keys:
                    if key == "time":
                        if key in data1:
                            date = datetime.datetime.fromtimestamp(data1[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
                            gold_data["update_time"] = date
                        else:
                            gold_data["update_time"] = "N/A"
                    else:
                        if key == "showName":
                            gold_data["name"] = data1.get(key, "黄金9999")
                        elif key == "q63":
                            gold_data["price"] = str(round(data1.get(key, "N/A"), 2)) if not isinstance(data1.get(key, "N/A"), str) else data1.get(key, "N/A")
                        elif key == "q70":
                            gold_data["change"] = str(round(data1.get(key, "N/A"), 2)) if not isinstance(data1.get(key, "N/A"), str) else data1.get(key, "N/A")
                        elif key == "q80":
                            value = data1.get(key, "N/A")
                            gold_data["change_rate"] = str(round(value, 2)) + "%" if not isinstance(value, str) else value
                        elif key == "q1":
                            gold_data["open"] = str(round(data1.get(key, "N/A"), 2)) if not isinstance(data1.get(key, "N/A"), str) else data1.get(key, "N/A")
                        elif key == "q3":
                            gold_data["high"] = str(round(data1.get(key, "N/A"), 2)) if not isinstance(data1.get(key, "N/A"), str) else data1.get(key, "N/A")
                        elif key == "q4":
                            gold_data["low"] = str(round(data1.get(key, "N/A"), 2)) if not isinstance(data1.get(key, "N/A"), str) else data1.get(key, "N/A")
                        elif key == "q2":
                            gold_data["prev_close"] = str(round(data1.get(key, "N/A"), 2)) if not isinstance(data1.get(key, "N/A"), str) else data1.get(key, "N/A")
                        elif key == "unit":
                            gold_data["unit"] = data1.get(key, "元/克")
                result.append(gold_data)
            
            # 现货黄金
            if "JO_92233" in data:
                data2 = data["JO_92233"]
                keys = ["showName", "q63", "q70", "q80", "q1", "q3", "q4", "q2", "time", "unit"]
                gold_data = {}
                for key in keys:
                    if key == "time":
                        if key in data2:
                            date = datetime.datetime.fromtimestamp(data2[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
                            gold_data["update_time"] = date
                        else:
                            gold_data["update_time"] = "N/A"
                    else:
                        if key == "showName":
                            gold_data["name"] = data2.get(key, "现货黄金")
                        elif key == "q63":
                            gold_data["price"] = str(round(data2.get(key, "N/A"), 2)) if not isinstance(data2.get(key, "N/A"), str) else data2.get(key, "N/A")
                        elif key == "q70":
                            gold_data["change"] = str(round(data2.get(key, "N/A"), 2)) if not isinstance(data2.get(key, "N/A"), str) else data2.get(key, "N/A")
                        elif key == "q80":
                            value = data2.get(key, "N/A")
                            gold_data["change_rate"] = str(round(value, 2)) + "%" if not isinstance(value, str) else value
                        elif key == "q1":
                            gold_data["open"] = str(round(data2.get(key, "N/A"), 2)) if not isinstance(data2.get(key, "N/A"), str) else data2.get(key, "N/A")
                        elif key == "q3":
                            gold_data["high"] = str(round(data2.get(key, "N/A"), 2)) if not isinstance(data2.get(key, "N/A"), str) else data2.get(key, "N/A")
                        elif key == "q4":
                            gold_data["low"] = str(round(data2.get(key, "N/A"), 2)) if not isinstance(data2.get(key, "N/A"), str) else data2.get(key, "N/A")
                        elif key == "q2":
                            gold_data["prev_close"] = str(round(data2.get(key, "N/A"), 2)) if not isinstance(data2.get(key, "N/A"), str) else data2.get(key, "N/A")
                        elif key == "unit":
                            gold_data["unit"] = data2.get(key, "美元/盎司")
                result.append(gold_data)
            
            # 现货白银
            if "JO_92232" in data:
                data3 = data["JO_92232"]
                keys = ["showName", "q63", "q70", "q80", "q1", "q3", "q4", "q2", "time", "unit"]
                gold_data = {}
                for key in keys:
                    if key == "time":
                        if key in data3:
                            date = datetime.datetime.fromtimestamp(data3[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
                            gold_data["update_time"] = date
                        else:
                            gold_data["update_time"] = "N/A"
                    else:
                        if key == "showName":
                            gold_data["name"] = data3.get(key, "现货白银")
                        elif key == "q63":
                            gold_data["price"] = str(round(data3.get(key, "N/A"), 2)) if not isinstance(data3.get(key, "N/A"), str) else data3.get(key, "N/A")
                        elif key == "q70":
                            gold_data["change"] = str(round(data3.get(key, "N/A"), 2)) if not isinstance(data3.get(key, "N/A"), str) else data3.get(key, "N/A")
                        elif key == "q80":
                            value = data3.get(key, "N/A")
                            gold_data["change_rate"] = str(round(value, 2)) + "%" if not isinstance(value, str) else value
                        elif key == "q1":
                            gold_data["open"] = str(round(data3.get(key, "N/A"), 2)) if not isinstance(data3.get(key, "N/A"), str) else data3.get(key, "N/A")
                        elif key == "q3":
                            gold_data["high"] = str(round(data3.get(key, "N/A"), 2)) if not isinstance(data3.get(key, "N/A"), str) else data3.get(key, "N/A")
                        elif key == "q4":
                            gold_data["low"] = str(round(data3.get(key, "N/A"), 2)) if not isinstance(data3.get(key, "N/A"), str) else data3.get(key, "N/A")
                        elif key == "q2":
                            gold_data["prev_close"] = str(round(data3.get(key, "N/A"), 2)) if not isinstance(data3.get(key, "N/A"), str) else data3.get(key, "N/A")
                        elif key == "unit":
                            gold_data["unit"] = data3.get(key, "美元/盎司")
                result.append(gold_data)
        
        print(f"获取到 {len(result)} 条实时贵金属数据")
        # 确保返回的JSON数据中中文字符正确编码
        import json
        # 先序列化再反序列化，确保编码正确
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        return json.loads(json_str)
    except Exception as e:
        print(f"获取实时贵金属价格失败: {e}")
        # 返回模拟数据作为 fallback
        import datetime
        now = datetime.datetime.now()
        return [
            {
                "name": "黄金9999",
                "price": "1964.9",
                "change": "3.40",
                "change_rate": "1.76%",
                "open": "1919.8",
                "high": "1989.99",
                "low": "1980.9",
                "prev_close": "1930.9",
                "update_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                "unit": "元/克"
            },
            {
                "name": "现货黄金",
                "price": "4795.39",
                "change": "180.84",
                "change_rate": "3.91%",
                "open": "4670.61",
                "high": "4855.15",
                "low": "4664.74",
                "prev_close": "4633.35",
                "update_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                "unit": "美元/盎司"
            },
            {
                "name": "现货白银",
                "price": "81.27",
                "change": "2.13",
                "change_rate": "2.69%",
                "open": "79.19",
                "high": "85.65",
                "low": "79.19",
                "prev_close": "79.15",
                "update_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                "unit": "美元/盎司"
            }
        ]

@router.get("/sectors", response_model=Dict[str, Any])
async def get_sectors_data():
    """获取行业板块数据"""
    try:
        import requests
        import json
        
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
        # 确保使用正确的编码解析响应
        response.encoding = response.apparent_encoding
        data = response.json()
        
        bk_result = []
        if data.get("data"):
            diff = data["data"].get("diff", [])
            for bk in diff:
                ratio = str(bk.get("f3", "N/A")) + "%"
                add_market_cap = bk.get("f62", 0)
                add_market_cap = str(round(add_market_cap / 100000000, 2)) + "亿"
                add_market_cap2 = bk.get("f84", 0)
                add_market_cap2 = str(round(add_market_cap2 / 100000000, 2)) + "亿"
                
                bk_result.append({
                    "name": bk.get("f14", "未知板块"),
                    "change": ratio,
                    "main_inflow": add_market_cap,
                    "main_inflow_ratio": str(round(bk.get("f184", 0), 2)) + "%",
                    "small_inflow": add_market_cap2,
                    "small_inflow_ratio": str(round(bk.get("f87", 0), 2)) + "%"
                })
        
        # 按涨跌幅排序
        bk_result.sort(key=lambda x: float(x["change"].replace("%", "")) if x["change"] != "N/A%" else -999, reverse=True)
        
        # 构建返回数据
        sectors = []
        for item in bk_result[:10]:  # 只返回前10个板块
            sectors.append({
                "name": item["name"],
                "change": item["change"]
            })
        
        return {
            "sectors": sectors
        }
    except Exception as e:
        print(f"获取行业板块数据失败: {e}")
        # 返回模拟数据作为 fallback
        return {
            "sectors": [
                {"name": "医药制造", "change": "1.03%"},
                {"name": "互联网", "change": "0.92%"},
                {"name": "新能源", "change": "0.88%"},
                {"name": "贵金属", "change": "-6.53%"}
            ]
        }

@router.get("/sector", response_model=Dict[str, Any])
async def get_sector_funds(bk_id: str):
    """获取板块基金"""
    try:
        # 确定板块名称
        bk_name = bk_id
        if bk_id in id_map:
            # 如果是数字ID，获取对应的板块名称
            bk_name = id_map[bk_id]
        elif bk_id in BK_MAP:
            # 如果是板块名称，直接使用
            bk_name = bk_id
        
        # 获取基金数据
        results = get_sector_funds_data(bk_id)
        
        return {
            "bk_id": bk_id,
            "bk_name": bk_name,
            "results": results
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/news", response_model=List[Dict[str, str]])
async def get_news():
    """获取实时新闻数据"""
    try:
        import datetime
        
        # 使用news_fetcher获取快讯数据
        kx_list = news_fetcher.fetch_news(count=10)
        print(f"BaiduNewsFetcher获取到 {len(kx_list)} 条快讯")
        
        # 格式化新闻数据
        news_items = []
        for item in kx_list:
            try:
                # 提取时间和内容
                publish_time = item.get("publish_time", "")
                title = item.get("title", "")
                
                # 处理时间格式
                if publish_time:
                    # 转换时间戳为可读格式
                    try:
                        publish_time = datetime.datetime.fromtimestamp(int(publish_time))
                        time_str = publish_time.strftime("%H:%M:%S")
                    except:
                        # 如果时间格式不正确，使用当前时间
                        time_str = datetime.datetime.now().strftime("%H:%M:%S")
                else:
                    # 如果没有时间，使用当前时间
                    time_str = datetime.datetime.now().strftime("%H:%M:%S")
                
                # 确保内容不为空
                if not title:
                    # 尝试从content字段获取内容
                    if "content" in item and isinstance(item["content"], dict):
                        items = item["content"].get("items", [])
                        if items and isinstance(items[0], dict):
                            title = items[0].get("data", "")
                
                # 确保内容不为空
                if title:
                    news_items.append({
                        "time": time_str,
                        "content": title
                    })
            except Exception as e:
                print(f"处理快讯数据错误: {e}")
                continue
        
        # 如果没有获取到数据，返回模拟数据作为 fallback
        if not news_items:
            now = datetime.datetime.now()
            news_items = [
                {
                    "time": (now - datetime.timedelta(minutes=30)).strftime("%H:%M:%S"),
                    "content": "游戏股集体跳水，世纪华通跌超9%"
                },
                {
                    "time": (now - datetime.timedelta(minutes=25)).strftime("%H:%M:%S"),
                    "content": "寒武纪、沐曦等国产AI芯片股集体下跌"
                },
                {
                    "time": (now - datetime.timedelta(minutes=20)).strftime("%H:%M:%S"),
                    "content": "奥瑞德、合肥AI与大数据研究院等新设创投合伙企业"
                },
                {
                    "time": (now - datetime.timedelta(minutes=15)).strftime("%H:%M:%S"),
                    "content": "商业航天板块震荡上扬，巨力索具涨停创新高"
                },
                {
                    "time": (now - datetime.timedelta(minutes=10)).strftime("%H:%M:%S"),
                    "content": "港股恒生指数涨幅扩大至1%"
                }
            ]
        
        print(f"返回 {len(news_items)} 条新闻")
        return news_items
    except Exception as e:
        print(f"Error in get_news: {e}")
        # 发生错误时返回模拟数据
        import datetime
        now = datetime.datetime.now()
        return [
            {
                "time": now.strftime("%H:%M:%S"),
                "content": "新闻数据加载中..."
            }
        ]

def get_sector_funds_data(sector_id: str) -> List[List[str]]:
    """根据板块ID或名称获取基金数据"""
    try:
        # 确定板块代码
        bk_code = None
        if sector_id in id_map:
            # 如果是数字ID，获取对应的板块名称
            sector_name = id_map[sector_id]
            bk_code = BK_MAP.get(sector_name)
        elif sector_id in BK_MAP:
            # 如果是板块名称，直接获取代码
            sector_name = sector_id
            bk_code = BK_MAP.get(sector_name)
        else:
            # 尝试直接作为板块代码使用
            bk_code = sector_id
            sector_name = "未知板块"
        
        if not bk_code:
            return []
        
        # 构建API请求
        url = "https://fund.eastmoney.com/data/FundGuideapi.aspx"
        params = {
            "dt": "4",
            "sd": "",
            "ed": "",
            "tp": bk_code,
            "sc": "1n",
            "st": "desc",
            "pi": "1",
            "pn": "1000",
            "zf": "diy",
            "sh": "list",
            "rnd": str(random.random())
        }
        
        headers = {
            "Connection": "keep-alive",
            "Referer": "https://fund.eastmoney.com/daogou/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        
        # 发送请求
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        # 解析响应
        text = json.loads(response.text.replace("var rankData =", "").strip())
        datas = text.get("datas", [])
        
        # 格式化数据
        fund_results = []
        for data in datas:
            data_list = data.split(",")
            fund_results.append([
                (data_list[0] or "---"),
                (data_list[1] or "---"),
                (data_list[3] or "---"),
                (data_list[15] or "---"),
                (data_list[16] or "---") + "（" + (data_list[17] or "---") + "%）",
                (data_list[5] or "---") + "%",
                (data_list[6] or "---") + "%",
                (data_list[7] or "---") + "%",
                (data_list[8] or "---") + "%",
                (data_list[4] or "---") + "%",
                (data_list[9] or "---") + "%",
                (data_list[10] or "---") + "%",
                (data_list[11] or "---") + "%",
                (data_list[24] or "---") + "%"
            ])
        
        return fund_results
    except Exception as e:
        # 发生错误时返回空列表
        print(f"Error fetching sector funds: {e}")
        return []
