# -*- coding: UTF-8 -*-

from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.services.fund_service import FundService
from app.services.calculator_service import CalculatorService
from app.utils.cache import CacheService

router = APIRouter()

# 初始化服务
fund_service = FundService()
cache_service = CacheService()
calculator_service = CalculatorService(cache_service=cache_service)

@router.get("/list", response_model=List[Dict[str, Any]])
async def get_funds_list():
    """获取基金列表"""
    try:
        print("获取基金列表")
        # 获取所有基金代码
        funds_data = cache_service.get_all()
        print(f"当前缓存: {funds_data}")
        
        # 收盘后更新持有金额，包含前一天的收益
        funds_data = calculator_service.update_hold_amount_after_market_close(funds_data)
        # 交易时段更新temp_amount
        funds_data = calculator_service.update_temp_amount_during_trading_hours(funds_data)
        # 保存更新后的缓存
        cache_service.update(funds_data)
        cache_service.save_cache()
        print(f"更新后缓存: {funds_data}")
        # 重新加载缓存，确保数据已保存
        cache_service.load_cache()
        print(f"重新加载后缓存: {cache_service.get_all()}")
        
        fund_codes = [code for code in funds_data.keys() if code not in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate", "last_update_date"]]
        print(f"基金代码: {fund_codes}")
        
        # 批量获取基金数据
        funds_info = fund_service.get_multiple_funds_data(fund_codes)
        print(f"基金数据: {funds_info}")
        
        # 计算盈亏
        for fund_info in funds_info:
            try:
                fund_code = fund_info.get("fund_code")
                if fund_code and fund_code in funds_data:
                    # 获取持有金额
                    hold_amount = funds_data[fund_code].get("hold_amount", 0.0)
                    # 获取基金名称
                    fund_name = funds_data[fund_code].get("fund_name", fund_code)
                    # 获取估值涨跌幅
                    forecast_growth = fund_info.get("forecast_growth", "N/A")
                    # 计算盈亏
                    profit_loss = calculator_service.calculate_profit_loss(hold_amount, forecast_growth)
                    
                    # 直接使用天天基金网API获取实时估值数据
                    try:
                        import requests
                        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
                        print(f"直接请求天天基金网API: {url}")
                        response = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                            "Referer": "http://fund.eastmoney.com/"
                        }, timeout=10, verify=False)
                        print(f"响应状态码: {response.status_code}")
                        print(f"响应内容: {response.text}")
                        
                        if response.status_code == 200:
                            content = response.text
                            print(f"原始响应内容: {repr(content)}")
                            # 使用更宽松的判断方式
                            content_stripped = content.strip()
                            print(f"去除空格后的内容: {repr(content_stripped)}")
                            if content_stripped.startswith('jsonpgz(') and content_stripped.endswith(');'):
                                # 去除jsonpgz(...)包装
                                json_content = content_stripped[8:-2]
                                print(f"提取的JSON内容: {repr(json_content)}")
                                import json
                                try:
                                    api_data = json.loads(json_content)
                                    print(f"解析后的API数据: {api_data}")
                                    
                                    # 更新估值数据
                                    gszzl = api_data.get('gszzl', 'N/A')
                                    gztime = api_data.get('gztime', 'N/A')
                                    print(f"从API获取的数据: gszzl={gszzl}, gztime={gztime}")
                                    
                                    # 实时估值涨跌幅
                                    fund_info["forecast_growth"] = f"{gszzl}%" if gszzl != 'N/A' else 'N/A'
                                    fund_info["now_time"] = gztime.split(' ')[1] if gztime != 'N/A' and ' ' in gztime else 'N/A'
                                    # 实际日涨幅（从fund_service获取的历史数据中获取）
                                    # 这里不更新day_of_growth，因为已经在fund_service中正确设置了
                                    
                                    # 重新计算盈亏
                                    forecast_growth = fund_info.get("forecast_growth", "N/A")
                                    # 使用hold_amount作为计算基础
                                    hold_amount = funds_data[fund_code].get("hold_amount", 0.0)
                                    profit_loss = calculator_service.calculate_profit_loss(hold_amount, forecast_growth)
                                    print(f"更新后的数据: forecast_growth={fund_info['forecast_growth']}, now_time={fund_info['now_time']}, day_of_growth={fund_info.get('day_of_growth', 'N/A')}, profit_loss={profit_loss}")
                                except Exception as json_error:
                                    print(f"JSON解析失败: {json_error}")
                                    import traceback
                                    traceback.print_exc()
                            else:
                                print(f"响应内容格式不正确，不是jsonpgz格式")
                    except Exception as e:
                        print(f"获取实时估值数据失败: {e}")
                    
                    fund_info["fund_name"] = fund_name
                    fund_info["hold_amount"] = hold_amount
                    fund_info["profit_loss"] = profit_loss
                    
                    # 将profit_loss和current_net_value存储到缓存中
                    funds_data[fund_code]["profit_loss"] = profit_loss
                    funds_data[fund_code]["current_net_value"] = fund_info.get("current_net_value", 0.0)
                    cache_service.update(funds_data)
                    cache_service.save_cache()
            except Exception as e:
                print(f"处理基金 {fund_code} 失败: {e}")
                import traceback
                traceback.print_exc()
        
        # 计算总持仓估值
        total_holdings = calculator_service.calculate_total_holdings_valuation(funds_data)
        # 更新总持仓数据到缓存
        funds_data.update(total_holdings)
        cache_service.update(funds_data)
        cache_service.save_cache()
        
        print(f"总持仓数据: {total_holdings}")
        print(f"返回数据: {funds_info}")
        return funds_info
    except Exception as e:
        print(f"获取基金列表失败: {e}")
        return [{"error": str(e)}]

@router.get("/total-info", response_model=Dict[str, Any])
async def get_total_info():
    """获取总持仓信息"""
    try:
        print("获取总持仓信息")
        # 重新加载缓存数据，确保使用最新的数据
        cache_service.load_cache()
        print("缓存重新加载完成")
        
        # 获取缓存数据
        funds_data = cache_service.get_all()
        print(f"当前缓存: {funds_data}")
        
        # 检查缓存数据是否包含总持仓信息
        has_total_hold_amount = "total_hold_amount" in funds_data
        has_total_profit_loss = "total_profit_loss" in funds_data
        has_total_valuation = "total_valuation" in funds_data
        has_total_profit_loss_rate = "total_profit_loss_rate" in funds_data
        
        print(f"缓存包含total_hold_amount: {has_total_hold_amount}")
        print(f"缓存包含total_profit_loss: {has_total_profit_loss}")
        print(f"缓存包含total_valuation: {has_total_valuation}")
        print(f"缓存包含total_profit_loss_rate: {has_total_profit_loss_rate}")
        
        # 获取总持仓信息
        total_hold_amount = funds_data.get("total_hold_amount", 0.0)
        total_profit_loss = funds_data.get("total_profit_loss", 0.0)
        total_valuation = funds_data.get("total_valuation", 0.0)
        total_profit_loss_rate = funds_data.get("total_profit_loss_rate", 0.0)
        
        # 打印详细信息
        print(f"总持仓金额: {total_hold_amount}")
        print(f"总盈亏: {total_profit_loss}")
        print(f"总估值: {total_valuation}")
        print(f"总盈亏率: {total_profit_loss_rate}")
        
        # 构建总持仓信息
        total_info = {
            "total_hold_amount": total_hold_amount,
            "total_profit_loss": total_profit_loss,
            "total_valuation": total_valuation,
            "total_profit_loss_rate": total_profit_loss_rate
        }
        print(f"总持仓信息: {total_info}")
        
        # 确保返回的是一个非空对象
        if not total_info:
            print("总持仓信息为空，返回默认值")
            total_info = {
                "total_hold_amount": 0.0,
                "total_profit_loss": 0.0,
                "total_valuation": 0.0,
                "total_profit_loss_rate": 0.0
            }
        
        print(f"最终返回的总持仓信息: {total_info}")
        return total_info
    except Exception as e:
        print(f"获取总持仓信息失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            "total_hold_amount": 0.0,
            "total_profit_loss": 0.0,
            "total_valuation": 0.0,
            "total_profit_loss_rate": 0.0
        }

@router.post("/add")
async def add_fund(fund_code: str):
    """添加基金"""
    try:
        print(f"添加基金: {fund_code}")
        # 获取基金数据
        fund_info = fund_service.get_fund_data(fund_code)
        print(f"基金数据: {fund_info}")
        
        # 添加到缓存
        funds_data = cache_service.get_all()
        print(f"当前缓存: {funds_data}")
        funds_data[fund_code] = {
            "fund_key": fund_code,  # 注意：这里可能需要基金的productId
            "fund_name": fund_info.get("fund_name", fund_code),
            "is_hold": False,
            "shares": 0,
            "cost_price": 0.0,
            "hold_amount": 0.0,
            "temp_amount": 0.0
        }
        cache_service.update(funds_data)
        print(f"更新后缓存: {cache_service.get_all()}")
        cache_service.save_cache()
        print("缓存保存完成")
        
        return {"message": "添加基金成功", "fund_code": fund_code}
    except Exception as e:
        print(f"添加基金失败: {e}")
        return {"error": str(e)}

@router.post("/delete")
async def delete_fund(fund_code: str):
    """删除基金"""
    try:
        # 从缓存中删除
        cache_service.delete(fund_code)
        cache_service.save_cache()
        
        return {"message": "删除基金成功", "fund_code": fund_code}
    except Exception as e:
        return {"error": str(e)}

@router.post("/set-hold-amount")
async def set_hold_amount(request_data: dict):
    """设置基金持有金额"""
    try:
        # 从请求体中获取参数
        fund_code = request_data.get("fund_code")
        amount = request_data.get("amount")
        
        if not fund_code or amount is None:
            return {"error": "缺少基金代码或持有金额"}
        
        # 转换amount为float类型
        try:
            amount = float(amount)
        except ValueError:
            return {"error": "持有金额必须是数字"}
        
        # 更新缓存
        funds_data = cache_service.get_all()
        if fund_code in funds_data:
            funds_data[fund_code]["hold_amount"] = amount
            funds_data[fund_code]["temp_amount"] = amount
            funds_data[fund_code]["is_hold"] = True
            cache_service.update(funds_data)
            cache_service.save_cache()
            return {"message": "设置持有金额成功", "fund_code": fund_code, "amount": amount}
        else:
            return {"error": "基金不存在"}
    except Exception as e:
        print(f"设置持有金额失败: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@router.get("/list/last", response_model=List[Dict[str, Any]])
async def get_funds_list_last():
    """获取盘后更新的基金列表"""
    try:
        print("获取盘后更新的基金列表")
        # 获取盘后更新的缓存数据
        last_funds_data = cache_service.get_last_all()
        print(f"盘后缓存: {last_funds_data}")
        
        fund_codes = [code for code in last_funds_data.keys() if code not in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate", "last_update_date"]]
        print(f"基金代码: {fund_codes}")
        
        # 批量获取基金数据
        funds_info = fund_service.get_multiple_funds_data(fund_codes)
        print(f"基金数据: {funds_info}")
        
        # 计算盈亏
        for fund_info in funds_info:
            fund_code = fund_info.get("fund_code")
            if fund_code and fund_code in last_funds_data:
                # 获取持有金额
                hold_amount = last_funds_data[fund_code].get("hold_amount", 0.0)
                # 获取基金名称
                fund_name = last_funds_data[fund_code].get("fund_name", fund_code)
                # 获取估值涨跌幅
                forecast_growth = fund_info.get("forecast_growth", "N/A")
                # 计算盈亏
                profit_loss = calculator_service.calculate_profit_loss(hold_amount, forecast_growth)
                
                fund_info["fund_name"] = fund_name
                fund_info["hold_amount"] = hold_amount
                fund_info["profit_loss"] = profit_loss
        
        print(f"返回数据: {funds_info}")
        return funds_info
    except Exception as e:
        print(f"获取盘后更新的基金列表失败: {e}")
        return [{"error": str(e)}]

@router.get("/{fund_code}", response_model=Dict[str, Any])
async def get_fund_detail(fund_code: str):
    """获取基金详情"""
    try:
        # 获取基金数据
        fund_info = fund_service.get_fund_data(fund_code)
        
        # 获取缓存中的持有金额
        funds_data = cache_service.get_all()
        if fund_code in funds_data:
            # 获取持有金额
            hold_amount = funds_data[fund_code].get("temp_amount", 0.0)
            # 获取估值涨跌幅
            forecast_growth = fund_info.get("forecast_growth", "N/A")
            # 计算盈亏
            profit_loss = calculator_service.calculate_profit_loss(hold_amount, forecast_growth)
            fund_info["hold_amount"] = hold_amount
            fund_info["profit_loss"] = profit_loss
        
        return fund_info
    except Exception as e:
        return {"error": str(e)}

@router.get("/{fund_code}/history", response_model=Dict[str, Any])
async def get_fund_history(fund_code: str, start_date: str = None, end_date: str = None):
    """获取基金历史净值数据"""
    try:
        print(f"获取基金 {fund_code} 的历史净值数据")
        # 获取历史净值数据
        history_data = fund_service.get_fund_history_nav(fund_code, start_date, end_date)
        
        # 获取基金基本信息
        fund_info = fund_service.get_fund_data(fund_code)
        
        # 构建返回数据
        result = {
            "fund_code": fund_code,
            "fund_info": fund_info,
            "history_data": history_data,
            "start_date": start_date or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": end_date or datetime.now().strftime("%Y-%m-%d"),
            "total_records": len(history_data)
        }
        
        print(f"返回历史净值数据: {len(history_data)} 条记录")
        return result
    except Exception as e:
        print(f"获取历史净值数据失败: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
