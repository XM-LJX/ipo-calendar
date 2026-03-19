# -*- coding: utf-8 -*-
"""
Alpha Vantage API 集成
用于：历史股价数据、保荐人胜率计算、IPO 回测
"""

import requests
import os
from datetime import datetime, timedelta
from config import TIMEOUT


class AlphaVantage:
    """Alpha Vantage API 客户端"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_KEY")
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_daily(self, symbol, market="US"):
        """
        获取日线数据
        
        Args:
            symbol: 股票代码（如：AAPL）
            market: 市场（US/HK/CN）
        
        Returns:
            dict: 日线数据
        """
        if not self.api_key:
            print("[Alpha Vantage] 未配置 API Key")
            return None
        
        # 处理不同市场的股票代码
        if market == "HK":
            symbol = f"{symbol}.HK"  # 港股格式
        elif market == "CN":
            print("[Alpha Vantage] A 股数据有限，建议使用东方财富")
            return None
        
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "apikey": self.api_key
        }
        
        try:
            print(f"[Alpha Vantage] 请求：{symbol}")
            response = requests.get(self.base_url, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if "Time Series (Daily)" in data:
                return data["Time Series (Daily)"]
            elif "Note" in data:
                print(f"[Alpha Vantage] API 限流：{data['Note']}")
                return None
            else:
                print(f"[Alpha Vantage] 无数据：{symbol}")
                return None
        except Exception as e:
            print(f"[Alpha Vantage] 错误：{e}")
            return None
    
    def get_sponsor_performance(self, sponsor_name, sample_stocks):
        """
        计算保荐人历史表现
        
        Args:
            sponsor_name: 保荐人名称
            sample_stocks: 该保荐人保荐的股票列表
        
        Returns:
            dict: 表现统计
        """
        if not sample_stocks:
            return {"win_rate": "N/A", "avg_return": "N/A"}
        
        total = 0
        wins = 0
        total_return = 0
        
        for stock in sample_stocks:
            symbol = stock.get("symbol")
            listing_date = stock.get("listing_date")
            
            if not symbol or not listing_date:
                continue
            
            # 获取上市后 5 日数据
            data = self.get_daily(symbol)
            if not data:
                continue
            
            try:
                # 计算上市后 5 日涨跌幅
                dates = sorted(data.keys())
                if len(dates) < 5:
                    continue
                
                first_day_close = float(data[dates[0]]["4. close"])
                fifth_day_close = float(data[dates[4]]["4. close"])
                
                return_pct = (fifth_day_close - first_day_close) / first_day_close
                
                total += 1
                total_return += return_pct
                if return_pct > 0:
                    wins += 1
            except (KeyError, ValueError) as e:
                print(f"[Alpha Vantage] 计算错误：{e}")
                continue
        
        if total == 0:
            return {"win_rate": "N/A", "avg_return": "N/A"}
        
        return {
            "win_rate": f"{wins/total*100:.1f}%",
            "avg_return": f"{total_return/total*100:.2f}%",
            "sample_size": total
        }
    
    def backtest_ipo(self, stock_list, hold_days=5):
        """
        IPO 回测
        
        Args:
            stock_list: IPO 股票列表
            hold_days: 持有天数
        
        Returns:
            dict: 回测结果
        """
        results = {
            "total": 0,
            "wins": 0,
            "avg_return": 0,
            "best": None,
            "worst": None
        }
        
        returns = []
        
        for stock in stock_list:
            symbol = stock.get("symbol")
            listing_date = stock.get("listing_date")
            
            if not symbol or not listing_date:
                continue
            
            data = self.get_daily(symbol)
            if not data:
                continue
            
            try:
                dates = sorted(data.keys())
                if len(dates) < hold_days:
                    continue
                
                first_close = float(data[dates[0]]["4. close"])
                hold_close = float(data[dates[hold_days-1]]["4. close"])
                
                return_pct = (hold_close - first_close) / first_close * 100
                
                returns.append(return_pct)
                results["total"] += 1
                
                if return_pct > 0:
                    results["wins"] += 1
                
                if results["best"] is None or return_pct > results["best"][1]:
                    results["best"] = (symbol, return_pct)
                
                if results["worst"] is None or return_pct < results["worst"][1]:
                    results["worst"] = (symbol, return_pct)
            
            except Exception as e:
                print(f"[回测] 错误：{e}")
                continue
        
        if returns:
            results["avg_return"] = sum(returns) / len(returns)
        
        return results
