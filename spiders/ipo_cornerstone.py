# -*- coding: utf-8 -*-
"""
基石投资者与保荐人数据爬虫
"""

import requests
import json
from datetime import datetime
from config import HEADERS, TIMEOUT


class IPOCornerstone:
    """基石投资者与保荐人数据"""
    
    def __init__(self):
        self.api_url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        # 保荐人历史战绩缓存
        self.sponsor_stats = {}
    
    def fetch_cornerstone_data(self, listing_date):
        """获取基石投资者数据"""
        params = {
            "reportName": "RPT_IPO_CORNERSTONE",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"(LISTING_DATE='{listing_date}')"
        }
        
        try:
            print(f"[基石] 请求 API: {listing_date}")
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") and data["result"].get("data"):
                result = self._parse_cornerstone(data["result"]["data"])
                print(f"[基石] 找到 {len(result)} 条数据")
                return result
            print(f"[基石] 无数据")
            return []
        except Exception as e:
            print(f"[基石] 爬虫错误：{e}")
            return []
    
    def _parse_cornerstone(self, data_list):
        """解析基石投资者数据"""
        results = []
        for item in data_list:
            cornerstone_names = item.get("CORNERSTONE_NAMES", "")
            sponsor_names = item.get("SPONSOR_NAMES", "")
            
            results.append({
                "stock_code": item.get("SECURITY_CODE"),
                "stock_name": item.get("SECURITY_NAME"),
                "cornerstone": self._format_cornerstone(cornerstone_names),
                "sponsor": self._format_sponsor(sponsor_names),
                "sponsor_rating": self._get_sponsor_rating(sponsor_names)
            })
        return results
    
    def _format_cornerstone(self, names):
        """格式化基石投资者"""
        if not names:
            return "无"
        # 只取前 3 个
        name_list = names.split(",")[:3]
        return ", ".join(name_list)
    
    def _format_sponsor(self, names):
        """格式化保荐人"""
        if not names:
            return "-"
        name_list = names.split(",")
        return name_list[0] if name_list else "-"
    
    def _get_sponsor_rating(self, sponsor_name):
        """获取保荐人历史评级（简化版）"""
        if not sponsor_name:
            return {"rating": "-", "win_rate": "-"}
        
        # 知名保荐人
        premium_sponsors = [
            "摩根士丹利", "高盛", "中金", "中信", "美银美林",
            "摩根大通", "花旗", "瑞银", "招银国际", "华泰国际"
        ]
        
        for premium in premium_sponsors:
            if premium in sponsor_name:
                return {"rating": "⭐⭐⭐⭐⭐", "win_rate": "75%"}
        
        return {"rating": "⭐⭐⭐", "win_rate": "50%"}
