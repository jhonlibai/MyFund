# -*- coding: UTF-8 -*-

import re
from typing import Dict, Any
from datetime import datetime

class CalculatorService:
    """基金计算服务"""
    
    def __init__(self, cache_service=None):
        self.cache_service = cache_service
    
    def calculate_profit_loss(self, hold_amount: float, forecast_growth: str) -> str:
        """计算基金盈亏"""
        try:
            if hold_amount <= 0 or forecast_growth == "N/A":
                return "0.00"
            
            # 提取数字部分
            matches = re.findall(r'-?\d+\.?\d*', forecast_growth)
            if not matches:
                return "0.00"
            
            # 取最后一个匹配项作为涨跌幅数值
            growth_rate = float(matches[-1])
            growth_rate = growth_rate / 100  # 转换为小数
            
            # 计算盈亏
            profit_loss = hold_amount * growth_rate
            
            # 格式化输出
            if profit_loss >= 0:
                return f"+{profit_loss:.2f}"
            else:
                return f"{profit_loss:.2f}"
        except Exception as e:
            print(f"计算盈亏失败: {e}")
            return "0.00"
    
    def calculate_total_holdings_valuation(self, funds_data: Dict[str, Any]) -> Dict[str, float]:
        """计算总持仓估值"""
        try:
            print(f"开始计算总持仓估值，funds_data: {funds_data}")
            total_hold = 0.0
            total_profit_loss = 0.0
            
            for fund_code, fund_info in funds_data.items():
                # 跳过总持仓相关字段
                if fund_code in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate", "last_update_date"]:
                    print(f"跳过总持仓相关字段: {fund_code}")
                    continue
                
                print(f"处理基金: {fund_code}, 基金信息: {fund_info}")
                # 获取持有金额和盈亏
                hold_amount = fund_info.get("temp_amount", 0.0)
                profit_loss = fund_info.get("profit_loss", 0.0)
                
                print(f"持有金额: {hold_amount}, 盈亏: {profit_loss}")
                # 累加总持仓
                total_hold += hold_amount
                print(f"累加后总持仓: {total_hold}")
                
                # 解析盈亏值
                if isinstance(profit_loss, str):
                    # 提取数字部分
                    matches = re.findall(r'-?\d+\.?\d*', profit_loss)
                    print(f"解析盈亏值，matches: {matches}")
                    if matches:
                        profit_loss_value = float(matches[-1])
                        total_profit_loss += profit_loss_value
                        print(f"解析后盈亏值: {profit_loss_value}, 累加后总盈亏: {total_profit_loss}")
                elif isinstance(profit_loss, float):
                    total_profit_loss += profit_loss
                    print(f"直接累加盈亏值: {profit_loss}, 累加后总盈亏: {total_profit_loss}")
            
            # 计算总估值
            total_valuation = total_hold + total_profit_loss
            print(f"计算总估值: {total_hold} + {total_profit_loss} = {total_valuation}")
            
            # 计算盈亏率
            total_profit_loss_rate = (total_profit_loss / total_hold * 100) if total_hold > 0 else 0.0
            print(f"计算盈亏率: {total_profit_loss_rate}")
            
            result = {
                "total_hold_amount": total_hold,
                "total_profit_loss": total_profit_loss,
                "total_valuation": total_valuation,
                "total_profit_loss_rate": total_profit_loss_rate
            }
            print(f"计算结果: {result}")
            return result
        except Exception as e:
            print(f"计算总持仓估值失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                "total_hold_amount": 0.0,
                "total_profit_loss": 0.0,
                "total_valuation": 0.0,
                "total_profit_loss_rate": 0.0
            }
    
    def update_hold_amount_after_market_close(self, funds_data: Dict[str, Any]) -> Dict[str, Any]:
        """收盘后更新持有金额"""
        try:
            # 获取当前时间
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            today = now.strftime("%Y-%m-%d")
            
            # 标记是否有更新
            has_updates = False
            
            # 为每个基金添加持仓日期并检查是否需要更新
            for fund_code, fund_info in funds_data.items():
                # 跳过总持仓相关字段
                if fund_code in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate"]:
                    continue
                
                # 如果没有hold_date，添加持仓日期
                if "hold_date" not in fund_info:
                    fund_info["hold_date"] = today
                    has_updates = True
                
                # 获取当前的估值涨跌幅
                current_forecast_growth = fund_info.get("forecast_growth", "")
                # 获取上一次的估值涨跌幅
                last_forecast_growth = fund_info.get("last_forecast_growth", "")
                
                # 检查是否在收盘后（16:00以后）
                if hour >= 16 or (hour == 15 and minute >= 30):
                    # 获取当前的hold_date、temp_amount和hold_amount
                    current_hold_date = fund_info.get("hold_date", "")
                    temp_amount = fund_info.get("temp_amount", 0.0)
                    hold_amount = fund_info.get("hold_amount", 0.0)
                    profit_loss = fund_info.get("profit_loss", 0.0)
                    
                    # 解析盈亏值
                    profit_loss_value = 0.0
                    if isinstance(profit_loss, str):
                        # 提取数字部分
                        matches = re.findall(r'-?\d+\.?\d*', profit_loss)
                        if matches:
                            profit_loss_value = float(matches[-1])
                    elif isinstance(profit_loss, float):
                        profit_loss_value = profit_loss
                    
                    # 只有在以下情况才更新：
                    # 1. hold_date不是当天（首次更新）
                    # 2. temp_amount不等于hold_amount（数值有变化）
                    # 3. 估值涨跌幅与上一次不一致
                    if current_hold_date != today or temp_amount != hold_amount or current_forecast_growth != last_forecast_growth:
                        # 更新hold_amount
                        new_hold_amount = temp_amount + profit_loss_value
                        fund_info["hold_amount"] = new_hold_amount
                        # 同时更新temp_amount，确保两个字段保持同步
                        fund_info["temp_amount"] = new_hold_amount
                        # 更新hold_date为当天
                        fund_info["hold_date"] = today
                        # 更新上一次的估值涨跌幅为当前值
                        fund_info["last_forecast_growth"] = current_forecast_growth
                        has_updates = True
                        print(f"基金【{fund_code}】收盘后持有金额已更新: {hold_amount:.2f} -> {new_hold_amount:.2f}")
                        print(f"估值涨跌幅变化: {last_forecast_growth} -> {current_forecast_growth}")
                else:
                    # 非收盘时间，只更新上一次的估值涨跌幅
                    if current_forecast_growth != last_forecast_growth:
                        fund_info["last_forecast_growth"] = current_forecast_growth
                        has_updates = True
            
            # 只有在有更新时才保存到缓存
            if has_updates and self.cache_service:
                self.cache_service.update(funds_data)
                self.cache_service.save_cache()
                # 同时保存到盘后更新缓存文件
                self.cache_service.save_last_cache(funds_data)
                print(f"收盘后持有金额已更新并保存到缓存和盘后缓存文件")
            elif not has_updates:
                print(f"无需更新持有金额，所有基金今日已更新且相关数值一致")
            
            return funds_data
        except Exception as e:
            print(f"更新持有金额失败: {e}")
            return funds_data
    
    def update_temp_amount_during_trading_hours(self, funds_data: Dict[str, Any]) -> Dict[str, Any]:
        """交易时段更新临时金额"""
        try:
            # 获取当前时间
            current_time = datetime.now().strftime("%H:%M")
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 检查是否需要在新的一天更新总持仓
            funds_data = self.update_hold_amount_on_new_day(funds_data)
            
            # 为每个基金添加持仓日期
            for fund_code, fund_info in funds_data.items():
                # 跳过总持仓相关字段
                if fund_code in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate"]:
                    continue
                
                # 添加持仓日期
                fund_info["hold_date"] = today
            
            # 检查是否在交易时段（08:00-16:00）
            if "08:00" <= current_time < "16:00":
                for fund_code, fund_info in funds_data.items():
                    # 跳过总持仓相关字段
                    if fund_code in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate"]:
                        continue
                    
                    # 获取hold_amount和temp_amount
                    hold_amount = fund_info.get("hold_amount", 0.0)
                    temp_amount = fund_info.get("temp_amount", 0.0)
                    
                    # 如果temp_amount不等于hold_amount，更新temp_amount
                    if temp_amount != hold_amount:
                        fund_info["temp_amount"] = hold_amount
                        print(f"基金【{fund_code}】temp_amount已更新: {temp_amount:.2f} -> {hold_amount:.2f}")
                
                # 更新总持仓的temp_hold_amount
                total_hold_amount = funds_data.get("total_hold_amount", 0.0)
                temp_hold_amount = funds_data.get("temp_hold_amount", 0.0)
                
                if temp_hold_amount != total_hold_amount:
                    funds_data["temp_hold_amount"] = total_hold_amount
                    print(f"temp_hold_amount已更新: {temp_hold_amount:.2f} -> {total_hold_amount:.2f}")
            
            # 如果有缓存服务，保存更新后的数据
            if self.cache_service:
                self.cache_service.update(funds_data)
                self.cache_service.save_cache()
                print(f"交易时段临时金额已更新并保存到缓存")
            
            return funds_data
        except Exception as e:
            print(f"更新临时金额失败: {e}")
            return funds_data
    
    def update_hold_amount_on_new_day(self, funds_data: Dict[str, Any]) -> Dict[str, Any]:
        """在新的一天更新持有金额为昨天的总估值"""
        try:
            # 获取当前日期
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 检查缓存中是否有last_update_date字段
            last_update_date = funds_data.get("last_update_date", "")
            
            # 如果last_update_date不是今天，说明是新的一天
            if last_update_date != today:
                print(f"新的一天，更新持有金额为昨天的总估值")
                
                # 获取昨天的总估值
                yesterday_total_valuation = funds_data.get("total_valuation", 0.0)
                print(f"昨天的总估值: {yesterday_total_valuation}")
                
                # 如果有总估值数据，更新持有金额
                if yesterday_total_valuation > 0:
                    # 更新每个基金的持有金额
                    total_hold_amount = funds_data.get("total_hold_amount", 0.0)
                    if total_hold_amount > 0:
                        # 按照比例更新每个基金的持有金额
                        for fund_code, fund_info in funds_data.items():
                            # 跳过总持仓相关字段
                            if fund_code in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate", "last_update_date"]:
                                continue
                            
                            # 获取当前持有金额
                            current_hold_amount = fund_info.get("hold_amount", 0.0)
                            # 计算比例
                            ratio = current_hold_amount / total_hold_amount
                            # 计算新的持有金额
                            new_hold_amount = yesterday_total_valuation * ratio
                            # 更新持有金额
                            fund_info["hold_amount"] = new_hold_amount
                            fund_info["temp_amount"] = new_hold_amount
                            print(f"基金【{fund_code}】持有金额已更新: {current_hold_amount:.2f} -> {new_hold_amount:.2f}")
                    else:
                        print("总持有金额为0，无法按比例更新")
                
                # 重新计算总持仓数据
                total_info = self.calculate_total_holdings_valuation(funds_data)
                funds_data.update(total_info)
                print(f"重新计算总持仓数据: {total_info}")
                
                # 更新last_update_date为今天
                funds_data["last_update_date"] = today
                print(f"更新last_update_date为: {today}")
            else:
                print("今日已更新持有金额，无需重复更新")
            
            return funds_data
        except Exception as e:
            print(f"在新的一天更新持有金额失败: {e}")
            return funds_data
