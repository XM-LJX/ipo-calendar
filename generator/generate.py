# -*- coding: utf-8 -*-
"""
HTML 页面生成器 v2.0 - 增强版
包含：暗盘数据、认购数据、基石投资者、日期选择
"""

import os
import json
from datetime import datetime, timedelta


def generate_html(data):
    """生成静态 HTML 页面"""
    
    # 生成日期选择器
    date_options = _generate_date_options(data['listing_date'])
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPO 日历 - {data['listing_date']}</title>
    <meta name="description" content="每日更新 A 股、港股 IPO 上市企业日历，{data['listing_date']}共{data['total']}家企业上市">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: white; color: #333; padding: 30px; border-radius: 15px; margin-bottom: 20px; 
                   box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; color: #667eea; }}
        .header .date {{ font-size: 24px; color: #666; margin: 10px 0; }}
        .header .update-time {{ font-size: 14px; color: #999; margin-top: 15px; }}
        .date-selector {{ margin: 20px 0; }}
        .date-selector select {{ padding: 10px 20px; font-size: 16px; border-radius: 8px; border: 2px solid #667eea; 
                                 background: white; cursor: pointer; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px; margin-bottom: 20px; }}
        .card {{ background: white; padding: 25px; border-radius: 15px; 
                 box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; }}
        .card h3 {{ color: #666; font-size: 14px; margin-bottom: 15px; }}
        .card .number {{ font-size: 48px; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .table-container {{ background: white; border-radius: 15px; 
                           padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                           margin-bottom: 20px; overflow-x: auto; }}
        .table-container h2 {{ margin-bottom: 20px; color: #333; font-size: 24px; }}
        table {{ width: 100%; border-collapse: collapse; min-width: 1200px; }}
        th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
              color: white; padding: 15px; text-align: left; font-weight: 600; 
              font-size: 14px; }}
        td {{ padding: 15px; border-bottom: 1px solid #f0f0f0; font-size: 14px; }}
        tr:hover {{ background: #f8f9fa; }}
        .market-tag {{ display: inline-block; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
        .market-a {{ background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #dc2626; }}
        .market-hk {{ background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); color: #2563eb; }}
        .darkpool-up {{ color: #dc2626; font-weight: bold; }}
        .darkpool-down {{ color: #16a34a; font-weight: bold; }}
        .hot-tag {{ background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white; 
                    padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
        .sponsor-tag {{ background: #f3f4f6; padding: 4px 12px; border-radius: 12px; font-size: 12px; }}
        .empty {{ text-align: center; padding: 60px 20px; color: #999; }}
        .footer {{ text-align: center; color: rgba(255,255,255,0.8); margin-top: 30px; }}
        .tooltip {{ position: relative; cursor: help; }}
        .tooltip:hover::after {{ content: attr(data-tip); position: absolute; bottom: 100%; left: 50%; 
                                  transform: translateX(-50%); background: #333; color: white; 
                                  padding: 8px 12px; border-radius: 6px; font-size: 12px; 
                                  white-space: nowrap; z-index: 100; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📅 IPO 日历</h1>
            <p class="date">上市日期：<span id="current-date">{data['listing_date']}</span></p>
            <p class="update-time">⏰ 更新时间：{data['update_time']}</p>
            
            <div class="date-selector">
                <label for="date-select">📅 选择日期：</label>
                <select id="date-select" onchange="location.href='?date='+this.value">
                    {date_options}
                </select>
            </div>
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
            {generate_a_stock_table(data['a_stock']) if data['a_stock'] else '<p class="empty">暂无 A 股 IPO 数据</p>'}
        </div>
        
        <div class="table-container">
            <h2>🇭🇰 港股 IPO <span style="font-size:16px;color:#666;">(含暗盘数据)</span></h2>
            {generate_hk_stock_table(data['hk_stock']) if data['hk_stock'] else '<p class="empty">暂无港股 IPO 数据</p>'}
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


def _generate_date_options(current_date):
    """生成日期选择器选项"""
    options = ""
    for i in range(-7, 8):  # 前后 7 天
        date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
        selected = "selected" if date == current_date else ""
        options += f'<option value="{date}" {selected}>{date}</option>\n'
    return options


def generate_a_stock_table(data_list):
    """生成 A 股表格"""
    if not data_list:
        return '<p class="empty">暂无数据</p>'
    
    rows = ""
    for item in data_list:
        # 认购数据
        sub = item.get("subscription", {})
        sub_text = f"{sub.get('oversubscription', '-')} | {sub.get('winning_rate', '-')}" if sub else "-"
        
        # 基石数据
        corner = item.get("cornerstone", {})
        cornerstone_text = corner.get("cornerstone", "-")
        sponsor_text = f"{corner.get('sponsor', '-')} {corner.get('sponsor_rating', '')}" if corner else "-"
        
        rows += f"""
        <tr>
            <td><span class="market-tag market-a">{item['market']}</span></td>
            <td><span style="font-family:monospace;">{item['stock_code']}</span></td>
            <td><strong>{item['stock_name']}</strong></td>
            <td>{item['exchange']}</td>
            <td>{item['issue_price']}</td>
            <td>{item['issue_volume']}</td>
            <td>{item['pe_ratio']}</td>
            <td>{sub_text}</td>
            <td>{cornerstone_text}</td>
            <td><span class="sponsor-tag">{sponsor_text}</span></td>
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
                <th>认购倍数 | 中签率</th>
                <th>基石投资者</th>
                <th>保荐人</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """


def generate_hk_stock_table(data_list):
    """生成港股表格（含暗盘数据）"""
    if not data_list:
        return '<p class="empty">暂无数据</p>'
    
    rows = ""
    for item in data_list:
        # 暗盘数据
        darkpool = item.get("dark_pool", {})
        if darkpool:
            dp_change = darkpool.get("dark_pool_change", "-")
            dp_class = "darkpool-up" if "+" in dp_change else "darkpool-down" if "-" in dp_change else ""
            darkpool_text = f"<span class='{dp_class}'>{dp_change}</span><br><small>{darkpool.get('dark_pool_close', '-')}</small>"
        else:
            darkpool_text = "-"
        
        # 认购数据
        sub = item.get("subscription", {})
        sub_text = f"{sub.get('oversubscription', '-')}<br><small>{sub.get('winning_rate', '-')}</small>" if sub else "-"
        hot_tag = '<span class="hot-tag">🔥 热门</span>' if sub.get("is_hot") else ""
        
        # 基石数据
        corner = item.get("cornerstone", {})
        cornerstone_text = corner.get("cornerstone", "-")
        sponsor_text = f"{corner.get('sponsor', '-')}<br><small>{corner.get('sponsor_rating', '')}</small>" if corner else "-"
        
        rows += f"""
        <tr>
            <td><span class="market-tag market-hk">{item['market']}</span></td>
            <td><span style="font-family:monospace;">{item['stock_code']}</span></td>
            <td><strong>{item['stock_name']}</strong> {hot_tag}</td>
            <td>{item['exchange']}</td>
            <td>{item['issue_price']}</td>
            <td>{item['issue_volume']}</td>
            <td>{darkpool_text}</td>
            <td>{sub_text}</td>
            <td>{cornerstone_text}</td>
            <td><span class="sponsor-tag">{sponsor_text}</span></td>
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
                <th>暗盘涨跌</th>
                <th>认购倍数<br><small>中签率</small></th>
                <th>基石投资者</th>
                <th>保荐人</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """


if __name__ == "__main__":
    # 测试用
    with open("data/ipo_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    generate_html(data)
