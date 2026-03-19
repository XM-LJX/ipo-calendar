# -*- coding: utf-8 -*-
"""
IPO Calendar 配置文件
"""

# 数据源配置
A_STOCK_API = "http://datacenter-web.eastmoney.com/api/data/v1/get"
HK_STOCK_API = "http://datacenter-web.eastmoney.com/api/data/v1/get"

# 输出配置
OUTPUT_DIR = "data"
HTML_OUTPUT = "index.html"

# 定时任务配置
UPDATE_TIME = "19:00"  # 每天 19 点更新

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://quote.eastmoney.com/"
}

# 超时设置
TIMEOUT = 10  # 秒
