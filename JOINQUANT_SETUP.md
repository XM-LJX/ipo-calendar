# 🔧 聚宽 JoinQuant 配置指南

## 📋 什么是聚宽？

**聚宽 JoinQuant** 是国内领先的量化交易平台，提供：
- ✅ 免费 A 股/港股/期货数据
- ✅ 在线策略研发和回测
- ✅ 模拟交易
- ✅ 丰富的因子库
- ✅ 活跃的量化社区

**官网**: https://www.joinquant.com/

---

## 🚀 快速开始

### 步骤 1: 注册账号

1. **访问官网**
   ```
   https://www.joinquant.com/
   ```

2. **微信扫码注册**
   - 点击右上角"登录/注册"
   - 选择"微信扫码登录"
   - 绑定手机号

3. **完善信息**
   - 填写基本信息
   - 完成风险测评

---

### 步骤 2: 获取 API Token

1. **登录后进入个人中心**
   ```
   https://www.joinquant.com/user
   ```

2. **查看 API Token**
   - 左侧菜单：设置 → API 设置
   - 复制你的 Token（格式：`xxxxxxxxxxxxxxxx`）

3. **配置到项目**
   ```bash
   cd /Users/henry/ipo-calendar
   vim .env
   ```
   
   添加：
   ```
   # 聚宽 API Token
   JOINQUANT_TOKEN=你的 Token
   ```

---

### 步骤 3: 创建第一个策略

1. **进入策略研究**
   ```
   https://www.joinquant.com/study
   ```

2. **新建 Notebook**
   - 点击"我的研究"
   - 点击"新建 Notebook"
   - 选择 Python 3 环境

3. **复制示例代码**
   ```python
   # 聚宽 IPO 策略示例
   
   # 导入聚宽 API
   from joinquant import *
   
   # 初始化
   def initialize(context):
       # 设置基准
       set_benchmark('000300.XSHG')
       # 设置佣金
       set_order_cost(OrderCost(open_tax=0, close_tax=0.001, 
                               open_commission=0.0003, 
                               close_commission=0.0003), 
                     type='stock')
       # 设置滑点
       set_slippage(PriceRelatedSlippage(0.002))
       
       # 持仓记录
       context.ipo_stocks = []
       context.max_position = 0.2
   
   # 每日运行
   def handle_data(context, data):
       # 获取 IPO 数据
       ipo_data = get_ipo_calendar()
       
       for stock_info in ipo_data:
           code = stock_info['code']
           score = calculate_score(stock_info)
           
           # 评分 > 80，买入
           if score >= 80:
               if code not in context.portfolio.positions:
                   buy_stock(context, code, score)
   
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
       
       # 保荐人（20 分）
       sponsor = stock_info.get('sponsor', '')
       if '摩根士丹利' in sponsor:
           score += 20
       elif '中金' in sponsor:
           score += 15
       
       # 基石投资者（10 分）
       cornerstone = stock_info.get('cornerstone', '')
       if '高瓴' in cornerstone:
           score += 10
       
       return score
   
   # 买入股票
   def buy_stock(context, code, score):
       # 计算仓位
       if score >= 80:
           position_ratio = 0.2
       elif score >= 60:
           position_ratio = 0.1
       else:
           position_ratio = 0.05
       
       # 下单
       available_cash = context.portfolio.available_cash
       buy_value = available_cash * position_ratio
       
       if buy_value > 1000:
           order_target_value(code, buy_value)
           log.info(f"买入 {code}，评分{score}")
   ```

4. **运行回测**
   - 点击"运行"
   - 选择时间范围（如：2025-01-01 到 2026-03-19）
   - 设置初始资金（如：100 万）
   - 查看回测结果

---

## 📊 聚宽 API 使用

### 本地调用示例

```python
# 安装聚宽 SDK
pip install joinquant

# 配置 Token
from joinquant import *

# 初始化
auth('你的用户名', '你的密码')

# 获取股票数据
def get_stock_data():
    # 获取 IPO 日历
    ipo_data = get_new_stocks()
    
    # 获取历史行情
    price_data = attribute_history('000001.XSHE', 100, '1d', ['open', 'close', 'high', 'low'])
    
    # 获取财务数据
    finance_data = get_fundamentals(query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio
    ).filter(
        valuation.code.in_(['000001.XSHE'])
    ))
    
    return ipo_data, price_data, finance_data
```

---

## 🎯 IPO 策略模板

### 策略 1: 暗盘跟风策略

```python
# 聚宽策略：暗盘跟风

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('策略启动')

def handle_data(context, data):
    # 获取今日 IPO 股票
    ipo_list = get_ipo_stocks()
    
    for stock in ipo_list:
        # 获取暗盘数据
        dark_pool = get_dark_pool_data(stock['code'])
        
        # 暗盘涨幅 > 10%，买入
        if dark_pool['change_pct'] > 10:
            order_target_value(stock['code'], 10000)
            log.info(f"买入 {stock['code']}，暗盘涨幅 {dark_pool['change_pct']}%")
```

---

### 策略 2: 超额认购策略

```python
# 聚宽策略：超额认购

def handle_data(context, data):
    # 获取 IPO 认购数据
    ipo_list = get_ipo_subscription()
    
    for stock in ipo_list:
        # 超额认购 > 100 倍，买入
        if stock['subscription_times'] > 100:
            order_target_value(stock['code'], 10000)
            log.info(f"买入 {stock['code']}，认购{stock['subscription_times']}倍")
```

---

### 策略 3: 综合评分策略

```python
# 聚宽策略：综合评分

def initialize(context):
    set_benchmark('000300.XSHG')
    context.max_hold = 5  # 最大持仓数

def handle_data(context, data):
    # 获取所有 IPO 股票
    ipo_list = get_all_ipo_data()
    
    # 计算每只股票评分
    scored_stocks = []
    for stock in ipo_list:
        score = calculate_composite_score(stock)
        scored_stocks.append((stock, score))
    
    # 按评分排序
    scored_stocks.sort(key=lambda x: x[1], reverse=True)
    
    # 买入前 5 名
    for i, (stock, score) in enumerate(scored_stocks[:context.max_hold]):
        if score >= 60:
            order_target_value(stock['code'], 20000)
            log.info(f"买入 #{i+1} {stock['code']} 评分{score}")

def calculate_composite_score(stock):
    score = 0
    
    # 暗盘涨幅（40 分）
    if stock.get('dark_pool_change', 0) > 15:
        score += 40
    elif stock.get('dark_pool_change', 0) > 10:
        score += 30
    
    # 认购倍数（30 分）
    if stock.get('subscription_times', 0) > 100:
        score += 30
    elif stock.get('subscription_times', 0) > 50:
        score += 20
    
    # 保荐人（20 分）
    sponsor = stock.get('sponsor', '')
    if '摩根士丹利' in sponsor:
        score += 20
    elif '中金' in sponsor:
        score += 15
    
    # 基石投资者（10 分）
    if '高瓴' in stock.get('cornerstone', ''):
        score += 10
    
    return score
```

---

## 📈 回测配置

### 基础回测参数

```python
# 回测配置
{
    "start_date": "2025-01-01",
    "end_date": "2026-03-19",
    "initial_cash": 1000000,  # 100 万
    "benchmark": "000300.XSHG",  # 沪深 300
    "frequency": "daily",
    "capacity": 10000000,  # 策略容量 1000 万
    "slippage": 0.002,  # 滑点 0.2%
    "commission": 0.0003  # 佣金万三
}
```

---

### 回测结果指标

| 指标 | 说明 | 优秀标准 |
|------|------|---------|
| **总收益率** | 策略总收益 | >20% |
| **年化收益** | 年化收益率 | >15% |
| **夏普比率** | 风险调整后收益 | >1.5 |
| **最大回撤** | 最大亏损幅度 | <-20% |
| **胜率** | 盈利交易占比 | >60% |
| **盈亏比** | 平均盈利/平均亏损 | >1.5 |

---

## 🎮 模拟交易

### 开启模拟交易

1. **进入模拟交易**
   ```
   https://www.joinquant.com/simulate
   ```

2. **创建模拟账户**
   - 点击"创建模拟账户"
   - 设置初始资金（建议 100 万）
   - 选择策略

3. **绑定实盘券商**（可选）
   - 支持：中信、华泰、国泰君安等
   - 模拟交易信号自动同步到实盘

---

## 📊 数据导入

### 导入 IPO Calendar 数据

```python
# 将 IPO Calendar 数据导入聚宽

import requests
import json

# 从 GitHub 获取数据
url = "https://raw.githubusercontent.com/XM-LJX/ipo-calendar/main/data/ipo_data.json"
response = requests.get(url)
data = json.loads(response.text)

# 处理数据
for stock in data['hk_stock']:
    code = stock['stock_code']
    dark_pool = stock.get('dark_pool', {})
    subscription = stock.get('subscription', {})
    
    # 在聚宽中记录
    record_ipo_data(code, dark_pool, subscription)
```

---

## 🔧 常见问题

### Q1: API Token 在哪里？

**A**: 登录后 → 个人中心 → 设置 → API 设置

### Q2: 数据准确吗？

**A**: 聚宽数据来自交易所，准确度很高

### Q3: 可以自动交易吗？

**A**: 
- 模拟交易：可以
- 实盘交易：需要绑定券商账户

### Q4: 免费额度够吗？

**A**: 
- 基础功能完全免费
- 高频数据需要付费
- 个人使用免费额度足够

---

## 🎯 快速开始清单

```
□ 1. 注册聚宽账号（微信扫码）
□ 2. 获取 API Token
□ 3. 配置到 .env 文件
□ 4. 创建第一个 Notebook
□ 5. 复制 IPO 策略代码
□ 6. 运行回测
□ 7. 开启模拟交易
□ 8. 观察表现
□ 9. 优化策略
□ 10. 考虑实盘
```

---

## 📚 学习资源

| 资源 | 链接 |
|------|------|
| **聚宽官网** | https://www.joinquant.com/ |
| **策略研究** | https://www.joinquant.com/study |
| **量化社区** | https://www.joinquant.com/community |
| **API 文档** | https://www.joinquant.com/help/api |
| **因子库** | https://www.joinquant.com/factor |

---

**配置完成后告诉我，我帮你创建策略！** 🎯
