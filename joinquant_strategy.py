# JoinQuant IPO 量化策略模板
# 复制此代码到聚宽：https://www.joinquant.com/

import pandas as pd
import numpy as np

# 初始化
def initialize(context):
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置佣金（万三）
    set_order_cost(OrderCost(
        open_tax=0,           # 买入无印花税
        close_tax=0.001,      # 卖出印花税 0.1%
        open_commission=0.0003,  # 买入佣金万三
        close_commission=0.0003, # 卖出佣金万三
        min_commission=5      # 最低 5 元
    ), type='stock')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 持仓记录
    context.ipo_stocks = []
    context.max_position = 0.2  # 单只股票最大仓位 20%
    
    # 定时运行（每天开盘前）
    run_daily(before_market_open, time='8:30')


# 开盘前处理
def before_market_open(context):
    # 获取 IPO 数据（需要自己导入）
    ipo_data = get_ipo_data()
    
    for stock_info in ipo_data:
        code = stock_info['code']
        score = calculate_score(stock_info)
        
        # 评分 > 80，强烈买入
        if score >= 80:
            if code not in context.portfolio.positions:
                buy_stock(context, code, score)
        
        # 评分 60-80，观望
        elif score >= 60:
            pass
        
        # 评分 < 60，卖出
        else:
            if code in context.portfolio.positions:
                sell_stock(context, code)


# 计算综合评分
def calculate_score(stock_info):
    score = 0
    
    # 暗盘涨幅（40 分）
    dark_pool = stock_info.get('dark_pool_change', 0)
    if dark_pool > 15:
        score += 40
    elif dark_pool > 10:
        score += 30
    elif dark_pool > 5:
        score += 20
    
    # 认购倍数（30 分）
    subscription = stock_info.get('subscription_times', 0)
    if subscription > 100:
        score += 30
    elif subscription > 50:
        score += 20
    elif subscription > 20:
        score += 10
    
    # 保荐人（20 分）
    sponsor = stock_info.get('sponsor', '')
    if '摩根士丹利' in sponsor or '高盛' in sponsor:
        score += 20
    elif '中金' in sponsor or '中信' in sponsor:
        score += 15
    
    # 基石投资者（10 分）
    cornerstone = stock_info.get('cornerstone', '')
    if '高瓴' in cornerstone or '红杉' in cornerstone:
        score += 10
    
    return score


# 买入股票
def buy_stock(context, code, score):
    # 计算买入数量（根据评分）
    if score >= 80:
        position_ratio = 0.2  # 重仓 20%
    elif score >= 60:
        position_ratio = 0.1  # 中仓 10%
    else:
        position_ratio = 0.05  # 轻仓 5%
    
    # 计算可用资金
    available_cash = context.portfolio.available_cash
    buy_value = available_cash * position_ratio
    
    # 下单
    if buy_value > 1000:  # 最小交易金额
        order_target_value(code, buy_value)
        log.info(f"买入 {code}，评分{score}，金额{buy_value}")


# 卖出股票
def sell_stock(context, code):
    # 检查止损
    if code in context.portfolio.positions:
        position = context.portfolio.positions[code]
        cost_basis = position.avg_cost
        current_price = position.price
        
        # 止损：亏损>10%
        if current_price < cost_basis * 0.9:
            order_target(code, 0)
            log.info(f"止损卖出 {code}，亏损{(current_price-cost_basis)/cost_basis:.2%}")
        
        # 止盈：盈利>20%
        elif current_price > cost_basis * 1.2:
            order_target(code, 0)
            log.info(f"止盈卖出 {code}，盈利{(current_price-cost_basis)/cost_basis:.2%}")


# 获取 IPO 数据（示例）
def get_ipo_data():
    # 这里需要导入 IPO Calendar 的数据
    # 可以手动上传 CSV 或通过 API 获取
    
    # 示例数据
    ipo_data = [
        {
            'code': '09999.HK',
            'name': '某某公司',
            'dark_pool_change': 15.32,
            'subscription_times': 150,
            'sponsor': '摩根士丹利',
            'cornerstone': '高瓴资本'
        },
        # ... 更多 IPO
    ]
    
    return ipo_data


# 每日收盘后记录
def after_market_close(context):
    # 记录当日持仓
    log.info(f"持仓数量：{len(context.portfolio.positions)}")
    for code, position in context.portfolio.positions.items():
        profit = (position.price - position.avg_cost) / position.avg_cost
        log.info(f"{code}: 盈利{profit:.2%}")
