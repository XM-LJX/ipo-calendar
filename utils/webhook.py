# -*- coding: utf-8 -*-
"""
Webhook 推送工具
支持：钉钉、企业微信、Server 酱
"""

import requests
import os
from config import TIMEOUT


def send_webhook(highlights):
    """发送 Webhook 推送"""
    if not highlights:
        print("[推送] 无亮点数据，跳过推送")
        return
    
    # 检查配置
    dingtalk_webhook = os.getenv("DINGTALK_WEBHOOK")
    wechat_webhook = os.getenv("WECHAT_WEBHOOK")
    serverchan_key = os.getenv("SERVERCHAN_KEY")
    
    message = _format_message(highlights)
    
    sent = False
    
    # 钉钉推送
    if dingtalk_webhook:
        try:
            _send_dingtalk(dingtalk_webhook, message)
            sent = True
        except Exception as e:
            print(f"[钉钉推送] 失败：{e}")
    
    # 企业微信推送
    if wechat_webhook:
        try:
            _send_wechat(wechat_webhook, message)
            sent = True
        except Exception as e:
            print(f"[企业微信推送] 失败：{e}")
    
    # Server 酱推送
    if serverchan_key:
        try:
            _send_serverchan(serverchan_key, message)
            sent = True
        except Exception as e:
            print(f"[Server 酱推送] 失败：{e}")
    
    if not sent:
        print("[推送] 未配置 Webhook，跳过")
    else:
        print(f"[推送] 已发送 {len(highlights)} 条亮点")


def _format_message(highlights):
    """格式化推送消息"""
    message = "📅 **IPO 日历 - 明日打新提醒**\n\n"
    message += "\n".join(highlights)
    message += f"\n\n📊 详细：https://XM-LJX.github.io/ipo-calendar/"
    return message


def _send_dingtalk(webhook, message):
    """发送钉钉机器人"""
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "IPO 日历提醒",
            "text": message
        }
    }
    response = requests.post(webhook, json=data, timeout=TIMEOUT)
    response.raise_for_status()
    print("[钉钉推送] 成功")


def _send_wechat(webhook, message):
    """发送企业微信机器人"""
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }
    response = requests.post(webhook, json=data, timeout=TIMEOUT)
    response.raise_for_status()
    print("[企业微信推送] 成功")


def _send_serverchan(key, message):
    """发送 Server 酱"""
    # 提取标题和正文
    lines = message.split("\n")
    title = lines[0].replace("📅 **", "").replace("**", "")
    content = "\n".join(lines[1:])
    
    params = {
        "title": title,
        "desp": content
    }
    url = f"https://sctapi.ftqq.com/{key}.send"
    response = requests.post(url, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    print("[Server 酱推送] 成功")
