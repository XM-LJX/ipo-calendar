# -*- coding: utf-8 -*-
"""
港股暗盘数据爬虫
数据源：东方财富网、富途牛牛
"""

import requests
import json
from datetime import datetime, timedelta
from config import HEADERS, TIMEOUT


class HKDarkPool:
    """港股暗盘数据爬虫"""
    
    def __init__(self):
        # 东方财富暗盘 API
        self.api_url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    
    def fetch_dark_pool_data(self, listing_date):
        """
        获取暗盘数据
        listing_date: 上市日期 YYYY-MM-DD
        暗盘交易时间：上市前一日 16:15-18:30
        """
        # 暗盘交易日期 = 上市日期 - 1 天
        dark_date = (datetime.strptime(listing_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        
        params = {
            "reportName": "RPT_IPO_DARKPOOL",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"(TRADE_DATE='{dark_date}')"
        }
        
        try:
            print(f"[暗盘] 请求 API: {dark_date}")
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") and data["result"].get("data"):
                result = self._parse_dark_pool(data["result"]["data"])
                print(f"[暗盘] 找到 {len(result)} 条数据")
                return result
            print(f"[暗盘] 无数据")
            return []
        except Exception as e:
            print(f"[暗盘] 爬虫错误：{e}")
            return []
    
    def _parse_dark_pool(self, data_list):
        """解析暗盘数据"""
        results = []
        for item in data_list:
            results.append({
                "stock_code": item.get("SECURITY_CODE"),
                "stock_name": item.get("SECURITY_NAME"),
                "dark_pool_close": self._format_price(item.get("DARK_POOL_CLOSE")),
                "dark_pool_change": self._format_change(item.get("DARK_POOL_CHANGE_PCT")),
                "dark_pool_volume": item.get("DARK_POOL_VOLUME", "-"),
                "broker": item.get("BROKER", "辉立证券")  # 默认辉立
            })
        return results
    
    def _format_price(self, price):
        """格式化价格"""
        if price is None:
            return "-"
        try:
            return f"HK${float(price):.2f}"
        except:
            return "-"
    
    def _format_change(self, change_pct):
        """格式化涨跌幅"""
        if change_pct is None:
            return "-"
        try:
            pct = float(change_pct)
            if pct > 0:
                return f"+{pct:.2f}%"
            else:
                return f"{pct:.2f}%"
        except:
            return "-"
