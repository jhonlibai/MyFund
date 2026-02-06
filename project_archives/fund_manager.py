# -*- coding: UTF-8 -*-

from loguru import logger


MAJOR_CATEGORIES = {
    "科技": ["人工智能", "半导体", "云计算", "5G", "光模块", "CPO", "F5G", "通信设备", "PCB", "消费电子",
            "计算机", "软件开发", "信创", "网络安全", "IT服务", "国产软件", "计算机设备", "光通信",
            "算力", "脑机接口", "通信", "电子", "光学光电子", "元件", "存储芯片", "第三代半导体",
            "光刻胶", "电子化学品", "LED", "毫米波", "智能穿戴", "东数西算", "数据要素", "国资云",
            "Web3.0", "AIGC", "AI应用", "AI手机", "AI眼镜", "DeepSeek", "TMT", "科技"],
    "医药健康": ["医药生物", "医疗器械", "生物疫苗", "CRO", "创新药", "精准医疗", "医疗服务", "中药",
                "化学制药", "生物制品", "基因测序", "超级真菌"],
    "消费": ["食品饮料", "白酒", "家用电器", "纺织服饰", "商贸零售", "新零售", "家居用品", "文娱用品",
            "婴童", "养老产业", "体育", "教育", "在线教育", "社会服务", "轻工制造", "新消费",
            "可选消费", "消费", "家电零部件", "智能家居"],
    "金融": ["银行", "证券", "保险", "非银金融", "国有大型银行", "股份制银行", "城商行", "金融"],
    "能源": ["新能源", "煤炭", "石油石化", "电力", "绿色电力", "氢能源", "储能", "锂电池", "电池",
            "光伏设备", "风电设备", "充电桩", "固态电池", "能源", "煤炭开采", "公用事业", "锂矿"],
    "工业制造": ["机械设备", "汽车", "新能源车", "工程机械", "高端装备", "电力设备", "专用设备",
            "通用设备", "自动化设备", "机器人", "人形机器人", "汽车零部件", "汽车服务",
            "汽车热管理", "尾气治理", "特斯拉", "无人驾驶", "智能驾驶", "电网设备", "电机",
            "高端制造", "工业4.0", "工业互联", "低空经济", "通用航空"],
    "材料": ["有色金属", "黄金股", "贵金属", "基础化工", "钢铁", "建筑材料", "稀土永磁", "小金属",
            "工业金属", "材料", "大宗商品", "资源"],
    "军工": ["国防军工", "航天装备", "航空装备", "航海装备", "军工电子", "军民融合", "商业航天",
            "卫星互联网", "航母", "航空机场"],
    "基建地产": ["建筑装饰", "房地产", "房地产开发", "房地产服务", "交通运输", "物流"],
    "环保": ["环保", "环保设备", "环境治理", "垃圾分类", "碳中和", "可控核聚变", "液冷"],
    "传媒": ["传媒", "游戏", "影视", "元宇宙", "超清视频", "数字孪生"],
    "主题": ["国企改革", "一带一路", "中特估", "中字头", "并购重组", "华为", "新兴产业",
            "国家安防", "安全主题", "农牧主题", "农林牧渔", "养殖业", "猪肉", "高端装备"]
}


class FundManager:
    
    def __init__(self, session, cache_map, csrf, save_cache_callback, format_table_callback):
        self.session = session
        self.CACHE_MAP = cache_map
        self._csrf = csrf
        self.save_cache = save_cache_callback
        self.format_table_msg = format_table_callback
    
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
    
    def mark_fund_sector(self):
        now_codes = list(self.CACHE_MAP.keys())
        logger.debug(f"当前缓存基金代码: {now_codes}")
        logger.info("请输入基金代码, 多个基金代码以英文逗号分隔:")
        codes = input()
        codes = codes.split(",")
        codes = [code.strip() for code in codes if code.strip()]

        all_sectors = []
        for category, sectors in MAJOR_CATEGORIES.items():
            for sector in sectors:
                all_sectors.append(sector)

        logger.info("板块分类列表:")
        results = []
        for i in range(0, len(all_sectors), 5):
            tmp = all_sectors[i:i + 5]
            tmp = [f"{i + 1 + j}. {tmp[j]}" for j in range(len(tmp))]
            results.append(tmp)
        for line_msg in self.format_table_msg(results).split("\n"):
            logger.info(line_msg)

        for code in codes:
            try:
                if code not in self.CACHE_MAP:
                    logger.warning(f"标记板块【{code}】失败: 不存在该基金代码, 请先添加该基金代码")
                    continue

                logger.info(f"为基金 【{code} {self.CACHE_MAP[code]['fund_name']}】 选择板块:")
                logger.info("请输入板块序号或自定义板块名称 (多个用逗号分隔, 如: 1,3,5 或 新能源,医药 或 1,新能源):")
                sector_input = input().strip()

                if sector_input:
                    sector_items = [s.strip() for s in sector_input.split(",")]
                    selected_sectors = []
                    for item in sector_items:
                        try:
                            idx = int(item)
                            if 1 <= idx <= len(all_sectors):
                                selected_sectors.append(all_sectors[idx - 1])
                            else:
                                selected_sectors.append(item)
                        except ValueError:
                            selected_sectors.append(item)

                    if selected_sectors:
                        self.CACHE_MAP[code]["sectors"] = selected_sectors
                        logger.info(f"✓ 已绑定板块: {', '.join(selected_sectors)}")
                    else:
                        logger.info("未选择任何板块")
                else:
                    logger.info("未选择任何板块")

                logger.info(f"标记板块【{code}】成功")

            except Exception as e:
                logger.error(f"标记板块【{code}】失败: {e}")
    
    def unmark_fund_sector(self):
        marked_codes = [code for code, data in self.CACHE_MAP.items() if data.get("sectors", [])]
        if not marked_codes:
            logger.warning("暂无板块标记的基金代码")
            return

        logger.debug(f"当前有板块标记的基金代码: {marked_codes}")
        logger.debug("请输入基金代码, 多个基金代码以英文逗号分隔:")
        codes = input()
        codes = codes.split(",")
        codes = [code.strip() for code in codes if code.strip()]

        for code in codes:
            try:
                if code in self.CACHE_MAP:
                    if self.CACHE_MAP[code].get("sectors", []):
                        self.CACHE_MAP[code]["sectors"] = []
                        logger.info(f"删除板块标记【{code}】成功")
                    else:
                        logger.warning(f"删除板块标记【{code}】失败: 该基金没有板块标记")
                else:
                    logger.warning(f"删除板块标记【{code}】失败: 不存在该基金代码")
            except Exception as e:
                logger.error(f"删除板块标记【{code}】失败: {e}")
    
    def set_hold_amount(self, set_hold_amount):
        try:
            items = set_hold_amount.split(",")
            for item in items:
                if "=" not in item:
                    logger.warning(f"格式错误: {item}，正确格式：基金代码=金额")
                    continue
                code, amount = item.split("=", 1)
                code = code.strip()
                amount = float(amount.strip())
                if code in self.CACHE_MAP:
                    self.CACHE_MAP[code]["hold_amount"] = amount
                    logger.info(f"设置基金【{code}】持有金额为 {amount} 元")
                else:
                    logger.warning(f"基金代码【{code}】不存在")
            logger.success("设置持有金额成功")
        except Exception as e:
            logger.error(f"设置持有金额失败: {e}")
    
    def set_cost_price(self, set_cost_price):
        try:
            items = set_cost_price.split(",")
            for item in items:
                if "=" not in item:
                    logger.warning(f"格式错误: {item}，正确格式：基金代码=成本价")
                    continue
                code, price = item.split("=", 1)
                code = code.strip()
                price = float(price.strip())
                if code in self.CACHE_MAP:
                    self.CACHE_MAP[code]["cost_price"] = price
                    logger.info(f"设置基金【{code}】买入成本价为 {price}")
                else:
                    logger.warning(f"基金代码【{code}】不存在")
            logger.success("设置买入成本价成功")
        except Exception as e:
            logger.error(f"设置买入成本价失败: {e}")
    
    def toggle_hold(self, codes):
        hold_codes = [code for code, data in self.CACHE_MAP.items() if data.get("is_hold", False)]
        if not hold_codes:
            logger.warning("暂无持有标注基金代码")
            return
        logger.debug(f"当前持有标注基金代码: {hold_codes}")
        logger.debug("请输入基金代码, 多个基金代码以英文逗号分隔:")
        codes = codes.split(",")
        codes = [code.strip() for code in codes if code.strip()]
        for code in codes:
            try:
                if code in self.CACHE_MAP:
                    self.CACHE_MAP[code]["is_hold"] = False
                    logger.info(f"删除持有标注【{code}】成功")
                else:
                    logger.warning(f"删除持有标注【{code}】失败: 不存在该基金代码")
            except Exception as e:
                logger.error(f"删除持有标注【{code}】失败: {e}")
    
    def toggle_not_hold(self, codes):
        hold_codes = [code for code, data in self.CACHE_MAP.items() if data.get("is_hold", False)]
        if not hold_codes:
            logger.warning("暂无持有标注基金代码")
            return
        logger.debug(f"当前持有标注基金代码: {hold_codes}")
        logger.debug("请输入基金代码, 多个基金代码以英文逗号分隔:")
        codes = codes.split(",")
        codes = [code.strip() for code in codes if code.strip()]
        for code in codes:
            try:
                if code in self.CACHE_MAP:
                    self.CACHE_MAP[code]["is_hold"] = False
                    logger.info(f"删除持有标注【{code}】成功")
                else:
                    logger.warning(f"删除持有标注【{code}】失败: 不存在该基金代码")
            except Exception as e:
                logger.error(f"删除持有标注【{code}】失败: {e}")
