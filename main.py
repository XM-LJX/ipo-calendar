#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPO Calendar 主程序
每天 19 点自动更新次日上市企业数据

使用方法:
    python main.py
"""

import json
import os
import sys
from datetime import datetime, timedelta

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spiders.a_stock import AStockIPO
from spiders.hk_stock import HKStockIPO
from generator.generate import generate_html


class IPOCalendar:
    """IPO 日历主程序"""
    
    def __init__(self):
        self.a_spider = AStockIPO()
        self.hk_spider = HKStockIPO()
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_all(self):
        """获取所有市场 IPO 数据"""
        print("=" * 60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始抓取 IPO 数据...")
        print("=" * 60)
        
        # 抓取 A 股
        a_data = self.a_spider.fetch_tomorrow_ipo()
        
        # 抓取港股
        hk_data = self.hk_spider.fetch_tomorrow_ipo()
        
        # 合并数据
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        all_data = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "listing_date": tomorrow,
            "a_stock": a_data,
            "hk_stock": hk_data,
            "total": len(a_data) + len(hk_data)
        }
        
        # 保存 JSON
        json_path = os.path.join(self.data_dir, "ipo_data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 数据已保存：{json_path}")
        
        # 生成 HTML
        generate_html(all_data)
        
        print("=" * 60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 更新完成！")
        print("=" * 60)
        
        return all_data


if __name__ == "__main__":
    try:
        calendar = IPOCalendar()
        calendar.fetch_all()
    except KeyboardInterrupt:
        print("\n❌ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
