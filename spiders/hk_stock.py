# -*- coding: utf-8 -*-
"""
港股 IPO 数据爬虫
数据源：东方财富网
"""

import requests
import json
from datetime import datetime, timedelta
from config import HK_STOCK_API, HEADERS, TIMEOUT


class HKStockIPO:
    """港股 IPO 数据爬虫"""
    
    def __init__(self):
        self.api_url = HK_STOCK_API
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    def fetch_tomorrow_ipo(self):
        """获取明日上市企业"""
        params = {
            "sortColumns": "LISTING_DATE",
            "sortTypes": "1",
            "pageSize": "50",
            "pageNumber": "1",
            "reportName": "RPT_HK_IPO_LISTING",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"(LISTING_DATE='{self.tomorrow}')"
        }
        
        try:
            print(f"[港股] 请求 API: {self.tomorrow}")
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") and data["result"].get("data"):
                # 数据校验
                validated = self._validate_hk_data(data["result"]["data"])
                result = self._parse_hk_stock(validated)
                print(f"[港股] 找到 {len(result)} 家企业")
                return result
            print(f"[港股] 无数据")
            return []
        except Exception as e:
            print(f"[港股] 爬虫错误：{e}")
            return []
    
    def _validate_hk_data(self, data_list):
        """校验港股数据（避免误匹配）"""
        validated = []
        for item in data_list:
            # 必须字段检查
            if not item.get("SECURITY_CODE"):
                print(f"[港股校验] 跳过：缺少代码 - {item.get('SECURITY_NAME')}")
                continue
            if not item.get("SECURITY_NAME"):
                print(f"[港股校验] 跳过：缺少名称")
                continue
            
            # 日期检查
            listing_date = item.get("LISTING_DATE", "")
            if listing_date != self.tomorrow:
                print(f"[港股校验] 跳过：日期不匹配 - {item.get('SECURITY_NAME')} ({listing_date})")
                continue
            
            # 港股代码格式检查（通常是 4-5 位数字）
            code = str(item.get("SECURITY_CODE", ""))
            if not code.isdigit() or len(code) < 4:
                print(f"[港股校验] 跳过：代码格式错误 - {code}")
                continue
            
            validated.append(item)
        
        return validated
    
    def _parse_hk_stock(self, data_list):
        """解析港股数据"""
        results = []
        for item in data_list:
            results.append({
                "market": "港股",
                "stock_code": item.get("SECURITY_CODE"),
                "stock_name": item.get("SECURITY_NAME"),
                "listing_date": item.get("LISTING_DATE"),
                "issue_price": self._format_price(item.get("ISSUE_PRICE")),
                "issue_volume": self._format_volume(item.get("ISSUE_VOLUME")),
                "pe_ratio": "-",  # 港股 IPO 通常不披露 PE
                "exchange": "港交所",
                "industry": item.get("INDUSTRY", "")
            })
        return results
    
    def _format_price(self, price):
        """格式化发行价（港币）"""
        if price is None:
            return "-"
        try:
            return f"HK${float(price):.2f}"
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
