# -*- coding: UTF-8 -*-

import json
import random
import requests
from loguru import logger
from module_html import get_table_html


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


class FundHTML:
    
    def __init__(self, cache_map, search_code_callback, major_categories):
        self.CACHE_MAP = cache_map
        self.search_code = search_code_callback
        self.MAJOR_CATEGORIES = major_categories
    
    def fund_html(self):
        result = self.search_code(True)
        logger.debug(f"fund_html: received {len(result)} results from search_code")
        logger.debug(f"fund_html: result before append={result}")
        
        total_hold = self.CACHE_MAP.get("total_hold_amount", 0.0)
        total_profit_loss = self.CACHE_MAP.get("total_profit_loss", 0.0)
        total_valuation = self.CACHE_MAP.get("total_valuation", 0.0)
        total_profit_loss_rate = self.CACHE_MAP.get("total_profit_loss_rate", 0.0)
        
        logger.debug(f"fund_html: total_hold={total_hold}, total_profit_loss={total_profit_loss}, total_valuation={total_valuation}")
        
        total_profit_display = f"+{total_profit_loss:.2f}" if total_profit_loss >= 0 else f"{total_profit_loss:.2f}"
        total_profit_rate_display = f"+{total_profit_loss_rate:.2f}%" if total_profit_loss_rate >= 0 else f"{total_profit_loss_rate:.2f}%"
        
        total_row = [
            "", 
            "总计", 
            "", 
            "", 
            "", 
            total_profit_rate_display, 
            "", 
            "", 
            f"{total_hold:.2f}", 
            total_profit_display,
            f"{total_valuation:.2f}"
        ]
        
        result.append(total_row)
        logger.debug(f"fund_html: total_row={total_row}")
        logger.debug(f"fund_html: result length after append={len(result)}")
        logger.debug(f"fund_html: result after append={result}")
        
        return get_table_html(
            [
                "基金代码", "基金名称", "估值时间", "估值", "日涨幅", "连涨/跌", "近30天", "持有", "盈亏", "总估值"
            ],
            result,
            sortable_columns=[3, 4, 5, 6, 7, 8, 9]
        )
    
    def select_fund_html(self, bk_id=None):
        if bk_id is None:
            data = self.select_fund(is_return=True)
            bk_list = data["bk_list"]

            buttons_html = '<div style="padding: 20px;">'
            for category, sectors in self.MAJOR_CATEGORIES.items():
                category_sectors = [(idx+1, name) for idx, name in enumerate(bk_list) if name in sectors]
                if not category_sectors:
                    continue

                buttons_html += f'<div style="margin-bottom: 25px;">'
                buttons_html += f'<h4 style="margin: 0 0 10px 0; color: #666; font-size: 14px; font-weight: 600;">{category}</h4>'
                buttons_html += '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px;">'

                for idx, bk_name in category_sectors:
                    buttons_html += f'''
                    <button onclick="loadSectorFunds('{idx}')"
                            style="padding: 10px; background: #fff; border: 1px solid #ddd;
                                   cursor: pointer; font-weight: 500; transition: all 0.2s;
                                   text-align: center; font-size: 13px; border-radius: 4px;"
                            onmouseover="this.style.background='#0070e0'; this.style.color='#fff'; this.style.borderColor='#0070e0'"
                            onmouseout="this.style.background='#fff'; this.style.color='#000'; this.style.borderColor='#ddd'">
                        {bk_name}
                    </button>
                    '''
                buttons_html += '</div></div>'
            buttons_html += '</div>'

            return f'''
            <div id="sector-selection">
                <h3 style="padding: 20px 20px 10px 20px; margin: 0; font-size: 1.2rem;">选择板块查看基金列表</h3>
                {buttons_html}
            </div>
            <div id="sector-funds-result"></div>
            <script>
            function loadSectorFunds(bkId) {{
                const resultDiv = document.getElementById('sector-funds-result');
                resultDiv.innerHTML = '<p style="padding: 20px; text-align: center;">加载中...</p>';
                resultDiv.scrollIntoView({{ behavior: 'smooth', block: 'start' }});

                fetch('/fund/sector?bk_id=' + bkId)
                    .then(response => response.text())
                    .then(html => {{
                        resultDiv.innerHTML = html;
                        autoColorize();
                        resultDiv.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    }})
                    .catch(error => {{
                        resultDiv.innerHTML = '<p style="padding: 20px; color: red;">加载失败: ' + error + '</p>';
                    }});
            }}
            </script>
            '''
        else:
            data = self.select_fund(bk_id=bk_id, is_return=True)
            if "error" in data:
                return f'<p style="color: red; padding: 20px;">{data["error"]}</p>'

            return f'''
            <div style="padding: 20px;">
                <h3 style="margin: 0 0 15px 0;">板块: {data["bk_name"]}</h3>
                {get_table_html(
                    ["基金代码", "基金名称", "基金类型", "日期", "净值|日增长率", "近1周", "近1月", "近3月", "近6月", "今年来", "近1年", "近2年", "近3年", "成立来"],
                    data["results"],
                    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                )}
            </div>
            '''
    
    @staticmethod
    def select_fund(bk_id=None, is_return=False):
        bk_map = BK_MAP
        bk_list = list(bk_map.keys())

        if is_return and bk_id is None:
            return {"bk_map": bk_map, "bk_list": bk_list}

        results = []
        id_map = {}
        for i in range(0, len(bk_list), 5):
            tmp = bk_list[i:i + 5]
            tmp = [str(i + 1 + j) + ". " + tmp[j] for j in range(len(tmp))]
            for j in range(len(tmp)):
                id_map[str(i + 1 + j)] = bk_map[bk_list[i + j]]
            results.append(tmp)

        if not is_return:
            for line_msg in format_table_msg(results).split("\n"):
                logger.info(line_msg)

            logger.debug("请输入要查询的板块序号(单选):")
            bk_id = input()
            while bk_id not in id_map:
                logger.error("输入有误, 请重新输入要查询的板块序号:")
                bk_id = input()

        if is_return and bk_id not in id_map:
            if bk_id in bk_map:
                bk_code = bk_map[bk_id]
            else:
                return {"error": "无效的板块ID或名称"}
        else:
            bk_code = id_map[bk_id]

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

        response = requests.get(url, headers=headers, params=params, timeout=30)
        text = json.loads(response.text.replace("var rankData =", "").strip())
        datas = text["datas"]
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

        if is_return:
            return {
                "bk_id": bk_id,
                "bk_name": list(bk_map.keys())[int(bk_id) - 1] if bk_id.isdigit() else bk_id,
                "results": fund_results
            }

        logger.critical(f"板块【{bk_id}. {list(bk_map.keys())[int(bk_id) - 1]}】基金列表:")
        for line_msg in format_table_msg([
            [
                "基金代码", "基金名称", "基金类型", "日期", "净值|日增长率", "近1周", "近1月", "近3月", "近6月",
                "今年来", "近1年", "近2年", "近3年", "成立来"
            ],
            *fund_results
        ]).split("\n"):
            logger.info(line_msg)
