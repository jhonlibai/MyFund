# -*- coding: UTF-8 -*-

from fastapi import APIRouter
from typing import Dict, Any
from app.services.calculator_service import CalculatorService
from app.utils.cache import CacheService

router = APIRouter()

# 初始化服务
cache_service = CacheService()
calculator_service = CalculatorService(cache_service=cache_service)

@router.get("/total", response_model=Dict[str, Any])
async def get_total_holdings():
    """获取总持仓信息"""
    try:
        # 重新加载缓存数据
        cache_service.load_cache()
        print("重新加载缓存数据")
        
        # 获取所有基金数据
        funds_data = cache_service.get_all()
        print(f"当前缓存数据: {funds_data}")
        
        # 计算总持仓估值
        total_info = calculator_service.calculate_total_holdings_valuation(funds_data)
        print(f"计算总持仓估值: {total_info}")
        
        # 更新缓存
        cache_service.update(total_info)
        cache_service.save_cache()
        print(f"更新缓存数据")
        
        return total_info
    except Exception as e:
        print(f"获取总持仓信息失败: {e}")
        return {"error": str(e)}

@router.post("/update")
async def update_holdings():
    """更新持仓信息"""
    try:
        # 获取所有基金数据
        funds_data = cache_service.get_all()
        
        # 更新临时金额（交易时段）
        funds_data = calculator_service.update_temp_amount_during_trading_hours(funds_data)
        
        # 更新持有金额（收盘后）
        funds_data = calculator_service.update_hold_amount_after_market_close(funds_data)
        
        # 计算总持仓估值
        total_info = calculator_service.calculate_total_holdings_valuation(funds_data)
        
        # 更新缓存
        funds_data.update(total_info)
        cache_service.update(funds_data)
        cache_service.save_cache()
        
        return {"message": "持仓信息更新成功", "total_info": total_info}
    except Exception as e:
        return {"error": str(e)}
