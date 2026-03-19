# -*- coding: utf-8 -*-
"""
IPO 量化交易策略引擎
"""

from datetime import datetime
from utils.alpha_vantage import AlphaVantage


class IPOStrategy:
    """IPO 交易策略基类"""
    
    def __init__(self):
        self.av = AlphaVantage()
    
    def generate_signal(self, stock_data):
        """
        生成交易信号
        
        Returns:
            dict: {
                "symbol": "09999.HK",
                "signal": "BUY/SELL/HOLD",
                "strength": "STRONG/MEDIUM/WEAK",
                "score": 85,
                "reason": "暗盘大涨 +15%，超额认购 150 倍"
            }
        """
        raise NotImplementedError


class DarkPoolStrategy(IPOStrategy):
    """暗盘跟风策略"""
    
    def generate_signal(self, stock_data):
        dark_pool = stock_data.get("dark_pool", {})
        change = dark_pool.get("dark_pool_change", "0%")
        
        # 解析涨跌幅
        try:
            pct = float(change.replace("+", "").replace("%", ""))
        except:
            pct = 0
        
        # 生成信号
        if pct > 15:
            return {
                "signal": "BUY",
                "strength": "STRONG",
                "score": 90,
                "reason": f"暗盘大涨 +{pct:.1f}%"
            }
        elif pct > 10:
            return {
                "signal": "BUY",
                "strength": "MEDIUM",
                "score": 75,
                "reason": f"暗盘上涨 +{pct:.1f}%"
            }
        elif pct > 5:
            return {
                "signal": "HOLD",
                "strength": "WEAK",
                "score": 50,
                "reason": f"暗盘微涨 +{pct:.1f}%"
            }
        else:
            return {
                "signal": "SELL",
                "strength": "MEDIUM",
                "score": 30,
                "reason": f"暗盘下跌 {pct:.1f}%"
            }


class SubscriptionStrategy(IPOStrategy):
    """超额认购策略"""
    
    def generate_signal(self, stock_data):
        sub = stock_data.get("subscription", {})
        oversub = sub.get("oversubscription", "0 倍")
        
        # 解析认购倍数
        try:
            times = float(oversub.replace("倍", "").replace("🔥", "").strip())
        except:
            times = 0
        
        if times > 100:
            return {
                "signal": "BUY",
                "strength": "STRONG",
                "score": 85,
                "reason": f"超额认购 {times:.0f}倍，市场情绪高涨"
            }
        elif times > 50:
            return {
                "signal": "BUY",
                "strength": "MEDIUM",
                "score": 65,
                "reason": f"超额认购 {times:.0f}倍"
            }
        elif times > 20:
            return {
                "signal": "HOLD",
                "strength": "WEAK",
                "score": 45,
                "reason": f"超额认购 {times:.0f}倍，情绪一般"
            }
        else:
            return {
                "signal": "SELL",
                "strength": "MEDIUM",
                "score": 25,
                "reason": f"认购不足 {times:.1f}倍"
            }


class SponsorStrategy(IPOStrategy):
    """保荐人胜率策略"""
    
    PREMIUM_SPONSORS = {
        "摩根士丹利": 75,
        "高盛": 72,
        "中金": 68,
        "中信": 65,
        "摩根大通": 70,
        "花旗": 68,
        "瑞银": 65
    }
    
    def generate_signal(self, stock_data):
        cornerstone = stock_data.get("cornerstone", {})
        sponsor = cornerstone.get("sponsor", "")
        
        # 查找保荐人胜率
        win_rate = 50  # 默认
        for premium, rate in self.PREMIUM_SPONSORS.items():
            if premium in sponsor:
                win_rate = rate
                break
        
        if win_rate >= 70:
            return {
                "signal": "BUY",
                "strength": "STRONG",
                "score": 80,
                "reason": f"保荐人{ sponsor }，历史胜率{ win_rate }%"
            }
        elif win_rate >= 65:
            return {
                "signal": "BUY",
                "strength": "MEDIUM",
                "score": 65,
                "reason": f"保荐人{ sponsor }，历史胜率{ win_rate }%"
            }
        else:
            return {
                "signal": "HOLD",
                "strength": "WEAK",
                "score": 45,
                "reason": f"保荐人{ sponsor }，胜率一般"
            }


class CompositeStrategy(IPOStrategy):
    """综合评分策略"""
    
    def __init__(self):
        super().__init__()
        self.dark_pool = DarkPoolStrategy()
        self.subscription = SubscriptionStrategy()
        self.sponsor = SponsorStrategy()
    
    def generate_signal(self, stock_data):
        """
        综合评分系统
        
        权重:
        - 暗盘涨幅：40%
        - 认购倍数：30%
        - 保荐人：20%
        - 基石投资者：10%
        """
        signals = []
        
        # 获取各策略信号
        if "dark_pool" in stock_data:
            signals.append(self.dark_pool.generate_signal(stock_data))
        
        if "subscription" in stock_data:
            signals.append(self.subscription.generate_signal(stock_data))
        
        if "cornerstone" in stock_data:
            signals.append(self.sponsor.generate_signal(stock_data))
        
        if not signals:
            return {
                "signal": "HOLD",
                "strength": "WEAK",
                "score": 50,
                "reason": "数据不足"
            }
        
        # 计算加权评分
        weights = [0.4, 0.3, 0.2, 0.1]
        total_score = 0
        total_weight = 0
        
        reasons = []
        for i, signal in enumerate(signals):
            weight = weights[i] if i < len(weights) else 0.1
            total_score += signal["score"] * weight
            total_weight += weight
            reasons.append(signal["reason"])
        
        final_score = total_score / total_weight if total_weight > 0 else 50
        
        # 生成最终信号
        if final_score >= 80:
            signal = "BUY"
            strength = "STRONG"
        elif final_score >= 60:
            signal = "BUY"
            strength = "MEDIUM"
        elif final_score >= 40:
            signal = "HOLD"
            strength = "WEAK"
        else:
            signal = "SELL"
            strength = "MEDIUM"
        
        return {
            "signal": signal,
            "strength": strength,
            "score": round(final_score, 1),
            "reason": " | ".join(reasons),
            "details": signals
        }
