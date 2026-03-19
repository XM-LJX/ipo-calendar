# -*- coding: utf-8 -*-
"""
IPO 认购数据爬虫
包含：超额认购倍数、中签率
"""

import requests
import json
from datetime import datetime
from config import HEADERS, TIMEOUT


class IPOSubscription:
    """IPO 认购数据爬虫"""
    
    def __init__(self):
        self.api_url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    
    def fetch_subscription_data(self, listing_date):
        """获取认购数据"""
        params = {
            "reportName": "RPT_IPO_SUBSCRIPTION",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"(LISTING_DATE='{listing_date}')"
        }
        
        try:
            print(f"[认购] 请求 API: {listing_date}")
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") and data["result"].get("data"):
                result = self._parse_subscription(data["result"]["data"])
                print(f"[认购] 找到 {len(result)} 条数据")
                return result
            print(f"[认购] 无数据")
            return []
        except Exception as e:
            print(f"[认购] 爬虫错误：{e}")
            return []
    
    def _parse_subscription(self, data_list):
        """解析认购数据"""
        results = []
        for item in data_list:
            # 超额认购倍数
            oversubscription = item.get("OVERSUBSCRIPTION_TIMES")
            # 中签率
            winning_rate = item.get("WINNING_RATE")
            
            results.append({
                "stock_code": item.get("SECURITY_CODE"),
                "stock_name": item.get("SECURITY_NAME"),
                "oversubscription": self._format_oversubscription(oversubscription),
                "winning_rate": self._format_winning_rate(winning_rate),
                "is_hot": self._is_hot(oversubscription)
            })
        return results
    
    def _format_oversubscription(self, times):
        """格式化超额认购倍数"""
        if times is None:
            return "未公布"
        try:
            t = float(times)
            if t >= 100:
                return f"🔥 {t:.0f}倍"
            elif t >= 50:
                return f"🔥 {t:.0f}倍"
            elif t >= 10:
                return f"{t:.0f}倍"
            else:
                return f"{t:.1f}倍"
        except:
            return "未公布"
    
    def _format_winning_rate(self, rate):
        """格式化中签率"""
        if rate is None:
            return "-"
        try:
            r = float(rate) * 100
            return f"{r:.2f}%"
        except:
            return "-"
    
    def _is_hot(self, times):
        """是否热门（超额认购>50 倍）"""
        if times is None:
            return False
        try:
            return float(times) >= 50
        except:
            return False
