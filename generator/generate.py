# -*- coding: utf-8 -*-
"""
HTML 页面生成器
"""

import os
from datetime import datetime


def generate_html(data):
    """生成静态 HTML 页面"""
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPO 日历 - 明日上市企业 ({data['listing_date']})</title>
    <meta name="description" content="每日更新 A 股、港股 IPO 上市企业日历，{data['listing_date']}共{data['total']}家企业上市">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: white; color: #333; padding: 30px; border-radius: 15px; margin-bottom: 20px; 
                   box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; color: #667eea; }}
        .header .date {{ font-size: 24px; color: #666; margin: 10px 0; }}
        .header .update-time {{ font-size: 14px; color: #999; margin-top: 15px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px; margin-bottom: 20px; }}
        .card {{ background: white; padding: 25px; border-radius: 15px; 
                 box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; }}
        .card h3 {{ color: #666; font-size: 14px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
        .card .number {{ font-size: 48px; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .table-container {{ background: white; border-radius: 15px; 
                           padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                           margin-bottom: 20px; overflow-x: auto; }}
        .table-container h2 {{ margin-bottom: 20px; color: #333; font-size: 24px; }}
        table {{ width: 100%; border-collapse: collapse; min-width: 800px; }}
        th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
              color: white; padding: 15px; text-align: left; font-weight: 600; 
              font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
        td {{ padding: 15px; border-bottom: 1px solid #f0f0f0; font-size: 14px; }}
        tr:hover {{ background: #f8f9fa; transition: background 0.2s; }}
        tr:last-child td {{ border-bottom: none; }}
        .market-tag {{ display: inline-block; padding: 6px 16px; 
                       border-radius: 20px; font-size: 12px; font-weight: 600; }}
        .market-a {{ background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #dc2626; }}
        .market-hk {{ background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); color: #2563eb; }}
        .empty {{ text-align: center; padding: 60px 20px; color: #999; font-size: 16px; }}
        .footer {{ text-align: center; color: rgba(255,255,255,0.8); margin-top: 30px; font-size: 14px; }}
        .stock-name {{ font-weight: 600; color: #333; }}
        .stock-code {{ color: #666; font-family: monospace; }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 24px; }}
            .card .number {{ font-size: 36px; }}
            .table-container {{ padding: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📅 IPO 日历</h1>
            <p class="date">明日上市企业：{data['listing_date']}</p>
            <p class="update-time">⏰ 更新时间：{data['update_time']}</p>
        </div>
        
        <div class="summary">
            <div class="card">
                <h3>总计</h3>
                <div class="number">{data['total']}</div>
            </div>
            <div class="card">
                <h3>🇨🇳 A 股</h3>
                <div class="number">{len(data['a_stock'])}</div>
            </div>
            <div class="card">
                <h3>🇭🇰 港股</h3>
                <div class="number">{len(data['hk_stock'])}</div>
            </div>
        </div>
        
        <div class="table-container">
            <h2>🇨🇳 A 股 IPO</h2>
            {generate_table(data['a_stock']) if data['a_stock'] else '<p class="empty">暂无 A 股 IPO 数据</p>'}
        </div>
        
        <div class="table-container">
            <h2>🇭🇰 港股 IPO</h2>
            {generate_table(data['hk_stock']) if data['hk_stock'] else '<p class="empty">暂无港股 IPO 数据</p>'}
        </div>
        
        <div class="footer">
            <p>数据来源：东方财富网 | 每天 19:00 自动更新</p>
            <p style="margin-top: 10px; opacity: 0.6;">© 2026 IPO Calendar | Built with ❤️</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存 HTML
    html_path = "index.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ HTML 已生成：{html_path}")


def generate_table(data_list):
    """生成表格 HTML"""
    if not data_list:
        return '<p class="empty">暂无数据</p>'
    
    rows = ""
    for item in data_list:
        market_class = "market-a" if item["market"] == "A 股" else "market-hk"
        rows += f"""
        <tr>
            <td><span class="market-tag {market_class}">{item['market']}</span></td>
            <td><span class="stock-code">{item['stock_code']}</span></td>
            <td><span class="stock-name">{item['stock_name']}</span></td>
            <td>{item['exchange']}</td>
            <td>{item['issue_price']}</td>
            <td>{item['issue_volume']}</td>
            <td>{item['pe_ratio']}</td>
        </tr>
        """
    
    return f"""
    <table>
        <thead>
            <tr>
                <th>市场</th>
                <th>代码</th>
                <th>名称</th>
                <th>交易所</th>
                <th>发行价</th>
                <th>发行量</th>
                <th>市盈率</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """


if __name__ == "__main__":
    # 测试用
    import json
    with open("data/ipo_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    generate_html(data)
