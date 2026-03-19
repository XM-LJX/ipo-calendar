#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPO Calendar 主程序 v2.0
增强版：暗盘数据 + 认购数据 + 基石投资者 + Webhook 推送

使用方法:
    python main.py
    python main.py --date 2026-03-20  # 查看指定日期
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spiders.a_stock import AStockIPO
from spiders.hk_stock import HKStockIPO
from spiders.hk_darkpool import HKDarkPool
from spiders.ipo_subscription import IPOSubscription
from spiders.ipo_cornerstone import IPOCornerstone
from generator.generate import generate_html
from utils.webhook import send_webhook

class IPOCalendar:
    """IPO 日历主程序 v2.0"""
    
    def __init__(self):
        self.a_spider = AStockIPO()
        self.hk_spider = HKStockIPO()
        self.darkpool_spider = HKDarkPool()
        self.subscription_spider = IPOSubscription()
        self.cornerstone_spider = IPOCornerstone()
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_all(self, target_date=None):
        """获取所有市场 IPO 数据"""
        print("=" * 60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始抓取 IPO 数据...")
        print("=" * 60)
        
        # 确定目标日期
        if target_date:
            listing_date = target_date
        else:
            listing_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        print(f"📅 上市日期：{listing_date}")
        
        # 1. 抓取基础 IPO 数据
        print("\n【1. 基础 IPO 数据】")
        a_data = self.a_spider.fetch_tomorrow_ipo()
        hk_data = self.hk_spider.fetch_tomorrow_ipo()
        
        # 2. 抓取暗盘数据（港股）
        print("\n【2. 暗盘数据】")
        darkpool_data = self.darkpool_spider.fetch_dark_pool_data(listing_date)
        
        # 3. 抓取认购数据
        print("\n【3. 认购数据】")
        subscription_data = self.subscription_spider.fetch_subscription_data(listing_date)
        
        # 4. 抓取基石投资者数据
        print("\n【4. 基石投资者】")
        cornerstone_data = self.cornerstone_spider.fetch_cornerstone_data(listing_date)
        
        # 合并数据
        all_data = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "listing_date": listing_date,
            "a_stock": self._merge_a_stock_data(a_data, subscription_data, cornerstone_data),
            "hk_stock": self._merge_hk_stock_data(hk_data, darkpool_data, subscription_data, cornerstone_data),
            "total": len(a_data) + len(hk_data)
        }
        
        # 保存 JSON
        json_path = os.path.join(self.data_dir, "ipo_data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 数据已保存：{json_path}")
        
        # 生成 HTML
        generate_html(all_data)
        
        # 发送 Webhook 推送
        highlights = self._get_highlights(all_data)
        if highlights:
            send_webhook(highlights)
        
        print("=" * 60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 更新完成！")
        print("=" * 60)
        
        return all_data
    
    def _merge_a_stock_data(self, a_data, sub_data, corner_data):
        """合并 A 股数据"""
        # 创建查找字典
        sub_dict = {item["stock_code"]: item for item in sub_data}
        corner_dict = {item["stock_code"]: item for item in corner_data}
        
        for item in a_data:
            code = item["stock_code"]
            if code in sub_dict:
                item["subscription"] = sub_dict[code]
            if code in corner_dict:
                item["cornerstone"] = corner_dict[code]
        
        return a_data
    
    def _merge_hk_stock_data(self, hk_data, darkpool_data, sub_data, corner_data):
        """合并港股数据（含暗盘）"""
        # 创建查找字典
        darkpool_dict = {item["stock_code"]: item for item in darkpool_data}
        sub_dict = {item["stock_code"]: item for item in sub_data}
        corner_dict = {item["stock_code"]: item for item in corner_data}
        
        for item in hk_data:
            code = item["stock_code"]
            # 合并暗盘数据
            if code in darkpool_dict:
                item["dark_pool"] = darkpool_dict[code]
            # 合并认购数据
            if code in sub_dict:
                item["subscription"] = sub_dict[code]
            # 合并基石数据
            if code in corner_dict:
                item["cornerstone"] = corner_dict[code]
        
        return hk_data
    
    def _get_highlights(self, data):
        """获取值得推送的亮点"""
        highlights = []
        
        # 检查港股暗盘
        for stock in data["hk_stock"]:
            if "dark_pool" in stock:
                dp = stock["dark_pool"]
                change = dp.get("dark_pool_change", "")
                if change != "-" and "+" in change:
                    pct = float(change.replace("+", "%").replace("%", ""))
                    if pct >= 10:
                        highlights.append(f"🔥 {stock['stock_name']} ({stock['stock_code']}) 暗盘大涨 {change}")
        
        return highlights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IPO Calendar v2.0")
    parser.add_argument("--date", type=str, help="查看指定日期的数据 (YYYY-MM-DD)")
    args = parser.parse_args()
    
    try:
        calendar = IPOCalendar()
        calendar.fetch_all(target_date=args.date)
    except KeyboardInterrupt:
        print("\n❌ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
