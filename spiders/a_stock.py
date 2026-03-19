# -*- coding: utf-8 -*-
"""
A 股 IPO 数据爬虫
数据源：东方财富网
"""

import requests
import json
from datetime import datetime, timedelta
from config import A_STOCK_API, HEADERS, TIMEOUT


class AStockIPO:
    """A 股 IPO 数据爬虫"""
    
    def __init__(self):
        self.api_url = A_STOCK_API
    
    def fetch_tomorrow_ipo(self):
        """获取明日上市企业"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        params = {
            "sortColumns": "LISTING_DATE",
            "sortTypes": "1",
            "pageSize": "50",
            "pageNumber": "1",
            "reportName": "RPT_SHARELISTING_DETAIL",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"(LISTING_DATE='{tomorrow}')"
        }
        
        try:
            print(f"[A 股] 请求 API: {tomorrow}")
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") and data["result"].get("data"):
                result = self._parse_a_stock(data["result"]["data"])
                print(f"[A 股] 找到 {len(result)} 家企业")
                return result
            print(f"[A 股] 无数据")
            return []
        except Exception as e:
            print(f"[A 股] 爬虫错误：{e}")
            return []
    
    def _parse_a_stock(self, data_list):
        """解析 A 股数据"""
        results = []
        for item in data_list:
            # 数据验证
            if not item.get("SECURITY_CODE") or not item.get("SECURITY_NAME"):
                continue
            
            results.append({
                "market": "A 股",
                "stock_code": item.get("SECURITY_CODE"),
                "stock_name": item.get("SECURITY_NAME"),
                "listing_date": item.get("LISTING_DATE"),
                "issue_price": self._format_price(item.get("ISSUE_PRICE")),
                "issue_volume": self._format_volume(item.get("PUBLIC_ISSUE_VOLUME")),
                "pe_ratio": self._format_pe(item.get("ISSUE_PE_RATIO")),
                "exchange": item.get("EXCHANGE", ""),
                "industry": item.get("CSRC_INDUSTRY", "")
            })
        return results
    
    def _format_price(self, price):
        """格式化发行价"""
        if price is None:
            return "-"
        try:
            return f"¥{float(price):.2f}"
        except:
            return "-"
    
    def _format_volume(self, volume):
        """格式化发行量"""
        if volume is None:
            return "-"
        try:
            vol = float(volume)
            if vol >= 100000000:
                return f"{vol/100000000:.2f}亿股"
            elif vol >= 10000:
                return f"{vol/10000:.2f}万股"
            else:
                return f"{vol}股"
        except:
            return "-"
    
    def _format_pe(self, pe):
        """格式化市盈率"""
        if pe is None:
            return "-"
        try:
            return f"{float(pe):.2f}倍"
        except:
            return "-"
