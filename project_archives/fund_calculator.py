# -*- coding: UTF-8 -*-

import datetime
import re
from loguru import logger


class FundCalculator:
    
    def __init__(self, cache_map, save_cache_callback, get_fund_forecast_callback):
        self.CACHE_MAP = cache_map
        self.save_cache = save_cache_callback
        self.get_fund_forecast_growth = get_fund_forecast_callback
    
    @staticmethod
    def calculate_profit_loss(hold_amount, forecast_growth):
        if hold_amount <= 0:
            return ""
        
        forecast_growth_value = forecast_growth
        
        if "\033" in forecast_growth_value:
            parts = forecast_growth_value.split("\033")
            forecast_growth_value = parts[-1] if len(parts) > 1 else parts[0]
        
        forecast_growth_value = forecast_growth_value.replace("%", "")
        
        if not forecast_growth_value or forecast_growth_value == "N/A":
            return ""
        
        try:
            matches = re.findall(r'-?\d+\.?\d*', forecast_growth_value)
            if not matches:
                return ""
            
            value_str = matches[-1]
            value = float(value_str)
            
            profit_loss_value = hold_amount * value / 100
            
            if profit_loss_value >= 0:
                return f"+{profit_loss_value:.2f}"
            else:
                return f"{profit_loss_value:.2f}"
        except (ValueError, AttributeError):
            return ""
    
    def update_temp_amount_during_trading_hours(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        if "08:00" <= current_time < "16:00":
            for fund in self.CACHE_MAP:
                if fund in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate"]:
                    continue
                if not isinstance(self.CACHE_MAP[fund], dict):
                    continue
                hold_amount = self.CACHE_MAP[fund].get("hold_amount", 0.0)
                temp_amount = self.CACHE_MAP[fund].get("temp_amount", 0.0)
                
                if temp_amount != hold_amount:
                    self.CACHE_MAP[fund]["temp_amount"] = hold_amount
                    logger.info(f"基金【{fund}】temp_amount已更新: {temp_amount:.2f} -> {hold_amount:.2f}")
            
            total_hold_amount = self.CACHE_MAP.get("total_hold_amount", 0.0)
            temp_hold_amount = self.CACHE_MAP.get("temp_hold_amount", 0.0)
            
            if temp_hold_amount != total_hold_amount:
                self.CACHE_MAP["temp_hold_amount"] = total_hold_amount
                logger.info(f"temp_hold_amount已更新: {temp_hold_amount:.2f} -> {total_hold_amount:.2f}")
            
            self.save_cache()
    
    def update_hold_amount_after_market_close(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time > "16:00":
            for fund in self.CACHE_MAP:
                if fund in ["total_hold_amount", "total_profit_loss", "temp_hold_amount", "total_valuation", "total_profit_loss_rate"]:
                    continue
                if not isinstance(self.CACHE_MAP[fund], dict):
                    continue
                temp_amount = self.CACHE_MAP[fund].get("temp_amount", 0.0)
                hold = self.CACHE_MAP[fund].get("hold_amount", 0.0)
                
                if temp_amount > 0:
                    forecast_growth = self.get_fund_forecast_growth(fund)
                    profit_loss_str = self.calculate_profit_loss(temp_amount, forecast_growth)
                    
                    if profit_loss_str:
                        try:
                            clean_profit_loss_str = profit_loss_str
                            if "\033" in clean_profit_loss_str:
                                parts = clean_profit_loss_str.split("\033")
                                clean_profit_loss_str = parts[-1] if len(parts) > 1 else parts[0]
                            matches = re.findall(r'-?\d+\.?\d*', clean_profit_loss_str)
                            if matches:
                                clean_profit_loss_str = matches[-1]
                            profit_loss_value = float(clean_profit_loss_str)
                            
                            new_hold_amount = temp_amount + profit_loss_value
                            if hold != new_hold_amount:
                                self.CACHE_MAP[fund]["hold_amount"] = new_hold_amount
                                logger.info(f"基金【{fund}】hold_amount已更新: {hold:.2f} -> {new_hold_amount:.2f}")
                        except ValueError:
                            pass
            self.save_cache()
    
    def calculate_total_holdings_valuation(self):
        total_hold = self.CACHE_MAP.get("total_hold_amount", 0.0)
        total_profit_loss = self.CACHE_MAP.get("total_profit_loss", 0.0)
        
        if total_hold > 0:
            total_valuation = total_hold + total_profit_loss
            profit_loss_rate = (total_profit_loss / total_hold) * 100
        else:
            total_valuation = 0.0
            profit_loss_rate = 0.0
        
        self.CACHE_MAP["total_valuation"] = total_valuation
        self.CACHE_MAP["total_profit_loss_rate"] = profit_loss_rate
        
        profit_rate_display = f"+{profit_loss_rate:.2f}%" if profit_loss_rate >= 0 else f"{profit_loss_rate:.2f}%"
        logger.info(f"总持仓估值: {total_valuation:.2f}元, 盈亏率: {profit_rate_display}")
        
        self.save_cache()
