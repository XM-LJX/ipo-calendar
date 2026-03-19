# 📚 聚宽 JQData API 完整使用手册

## 🎯 快速开始

### 1. 安装

```bash
pip install jqdatasdk
```

### 2. 认证

```python
from jqdatasdk import *

# 方式 1: 账号密码
auth('13606066742', 'SXM123456asd')

# 方式 2: Token
auth_token('你的 Token')
```

### 3. 测试

```python
# 获取平安银行行情
df = get_price('000001.XSHE', start_date='2025-01-01', end_date='2025-12-17')
print(df)
```

---

## 📊 核心 API 分类

### 一、行情数据 API ⭐⭐⭐⭐⭐

#### 1. get_price() - 获取行情数据

```python
# 基础用法
df = get_price('000001.XSHE', 
               start_date='2025-01-01', 
               end_date='2025-12-17')

# 多只股票
df = get_price(['000001.XSHE', '600519.XSHG'], 
               start_date='2025-01-01')

# 分钟线
df = get_price('000001.XSHE', 
               start_date='2025-01-01', 
               frequency='60m')  # 60 分钟线

# 周线/月线
df = get_price('000001.XSHE', 
               start_date='2025-01-01', 
               frequency='weekly')  # 周线
df = get_price('000001.XSHE', 
               start_date='2025-01-01', 
               frequency='monthly')  # 月线
```

**参数说明**:
| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| code | str/list | 股票代码 | '000001.XSHE' |
| start_date | str | 开始日期 | '2025-01-01' |
| end_date | str | 结束日期 | '2025-12-17' |
| frequency | str | 频率 | daily/60m/weekly/monthly |
| fields | list | 字段 | ['open','close','high','low','volume'] |
| skip_paused | bool | 是否跳过停牌 | True/False |
| fq | str | 复权 | pre(前复权)/post(后复权)/None |

**返回字段**:
```python
open      # 开盘价
close     # 收盘价
high      # 最高价
low       # 最低价
volume    # 成交量
money     # 成交额
factor    # 复权因子
paused    # 是否停牌
```

---

#### 2. get_ticks() - 获取 Tick 数据

```python
# 获取 1 分钟 Tick 数据
df = get_ticks('000001.XSHE', 
               start_date='2025-01-01', 
               end_date='2025-01-01', 
               fields=['time','price','volume'])
```

---

#### 3. get_current_tick() - 获取实时 Tick

```python
# 实时行情（需要付费版）
tick = get_current_tick('000001.XSHE')
print(tick)
```

---

#### 4. get_price_count() - 获取 K 线数量

```python
# 计算有多少条 K 线
count = get_price_count('000001.XSHE', 
                        start_date='2025-01-01', 
                        end_date='2025-12-17')
print(f"共{count}条 K 线")
```

---

### 二、财务数据 API ⭐⭐⭐⭐

#### 1. get_fundamentals() - 获取财务数据

```python
from jqdatasdk import query, valuation, income, balance, cash_flow

# 获取估值数据
df = get_fundamentals(query(
    valuation.code,
    valuation.pe_ratio,      # 市盈率
    valuation.pb_ratio,      # 市净率
    valuation.ps_ratio,      # 市销率
    valuation.market_cap,    # 总市值
    valuation.circulating_market_cap  # 流通市值
))

# 获取利润表数据
df = get_fundamentals(query(
    income.code,
    income.total_revenue,           # 营业总收入
    income.operating_profit,        # 营业利润
    income.net_profit,              # 净利润
    income.operating_cost           # 营业成本
))

# 获取资产负债表数据
df = get_fundamentals(query(
    balance.code,
    balance.total_assets,           # 资产总计
    balance.total_liability,        # 负债合计
    balance.equity,                 # 股东权益
    balance.retained_earnings       # 未分配利润
))

# 获取现金流量表数据
df = get_fundamentals(query(
    cash_flow.code,
    cash_flow.operating_cash_flow,       # 经营活动现金流
    cash_flow.investing_cash_flow,       # 投资活动现金流
    cash_flow.financing_cash_flow        # 筹资活动现金流
))
```

**查询条件**:
```python
# 筛选 PE < 20 的股票
df = get_fundamentals(query(
    valuation.code,
    valuation.pe_ratio
).filter(
    valuation.pe_ratio < 20
))

# 筛选市值 > 100 亿的股票
df = get_fundamentals(query(
    valuation.code,
    valuation.market_cap
).filter(
    valuation.market_cap > 10000000000  # 100 亿
))

# 筛选多个条件
df = get_fundamentals(query(
    valuation.code,
    valuation.pe_ratio,
    valuation.market_cap
).filter(
    valuation.pe_ratio < 30,
    valuation.market_cap > 5000000000
))

# IN 查询
df = get_fundamentals(query(
    valuation.code,
    valuation.pe_ratio
).filter(
    valuation.code.in_(['000001.XSHE', '600519.XSHG'])
))

# LIKE 查询
df = get_fundamentals(query(
    valuation.code
).filter(
    valuation.code.like('000%')  # 000 开头的股票
))
```

---

#### 2. get_fundamentals_continuously() - 获取连续财务数据

```python
# 获取贵州茅台连续 5 年的 PE
df = get_fundamentals_continuously(
    query(valuation.code, valuation.pe_ratio),
    day='2025-12-31',
    count=5,
    fields=['valuation.pe_ratio']
)
```

---

#### 3. get_valuation() - 获取历史估值

```python
# 获取某日期的估值数据
df = get_valuation(
    fields=['code', 'pe_ratio', 'pb_ratio'],
    date='2025-12-31'
)
```

---

### 三、指数数据 API ⭐⭐⭐⭐

#### 1. get_index_stocks() - 获取指数成分股

```python
# 获取沪深 300 成分股
hs300 = get_index_stocks('000300.XSHG')
print(f"沪深 300 共{len(hs300)}只成分股")

# 获取上证 50 成分股
sz50 = get_index_stocks('000016.XSHG')

# 获取中证 500 成分股
zz500 = get_index_stocks('000905.XSHG')
```

**常见指数代码**:
```python
# 宽基指数
'000300.XSHG'  # 沪深 300
'000016.XSHG'  # 上证 50
'000905.XSHG'  # 中证 500
'000001.XSHG'  # 上证指数
'399001.XSHE'  # 深证成指
'399006.XSHE'  # 创业板指

# 行业指数
'000037.XSHG'  # 380 金融
'000038.XSHG'  # 380 能源
'000039.XSHG'  # 380 材料
```

---

#### 2. get_index_weight() - 获取指数权重

```python
# 获取沪深 300 成分股权重
weight = get_index_weight('000300.XSHG', 
                          date='2025-12-31')
print(weight.head())
```

---

#### 3. get_index_price() - 获取指数行情

```python
# 获取沪深 300 历史行情
df = get_price('000300.XSHG', 
               start_date='2025-01-01', 
               end_date='2025-12-17')
```

---

### 四、基金数据 API ⭐⭐⭐

#### 1. get_fund_nav() - 获取基金净值

```python
# 获取基金净值
nav = get_fund_nav('000001')  # 华夏成长混合
print(nav)

# 获取多只基金
navs = get_fund_nav(['000001', '000002', '000003'])
```

---

#### 2. get_fund_info() - 获取基金信息

```python
# 获取基金基本信息
info = get_fund_info('000001')
print(info)
```

---

#### 3. get_fund_holdings() - 获取基金持仓

```python
# 获取基金重仓股
holdings = get_fund_holdings('000001', 
                              n=10)  # 前 10 大重仓
print(holdings)
```

---

### 五、IPO 数据 API ⭐⭐⭐⭐⭐

#### 1. get_new_stocks() - 获取新股发行

```python
# 获取某月新股
ipo = get_new_stocks('2025-01')  # 2025 年 1 月
print(ipo)

# 获取多个月份
ipo = get_new_stocks('2025-01', '2025-12')
print(f"2025 年共{len(ipo)}只 IPO")
```

**返回字段**:
```python
code          # 股票代码
name          # 股票名称
listing_date  # 上市日期
issue_price   # 发行价
issue_volume  # 发行量
market        # 市场（主板/创业板/科创板）
```

---

#### 2. get_new_stock_distribution() - 获取新股配售

```python
# 获取新股配售数据
dist = get_new_stock_distribution('000001.XSHE')
print(dist)
```

---

### 六、资金流向 API ⭐⭐⭐⭐

#### 1. get_money_flow() - 获取资金流向

```python
# 获取个股资金流向
flow = get_money_flow('000001.XSHE', 
                      start_date='2025-01-01', 
                      end_date='2025-12-17')
print(flow.head())

# 获取板块资金流向
flow = get_money_flow('000001.XSHE', 
                      type='sector')
```

**返回字段**:
```python
code                # 股票代码
time                # 时间
net_amount_main     # 主力净额
net_amount_big      # 超大单净额
net_amount_medium   # 大单净额
net_amount_small    # 中单净额
net_amount_trivial  # 小单净额
```

---

#### 2. get_stock_money_flow() - 获取个股资金流

```python
# 获取某日资金流
flow = get_stock_money_flow('000001.XSHE', 
                            date='2025-12-17')
```

---

#### 3. get_sector_money_flow() - 获取板块资金流

```python
# 获取行业资金流
flow = get_sector_money_flow('801010',  # 农林牧渔
                             date='2025-12-17')
```

---

### 七、宏观数据 API ⭐⭐⭐

#### 1. get_macro_data() - 获取宏观经济数据

```python
# 获取 GDP 数据
gdp = get_macro_data('M0000523')  # GDP 当季同比
print(gdp)

# 获取 CPI 数据
cpi = get_macro_data('M0000612')  # CPI 当月同比
print(cpi)

# 获取 M2 数据
m2 = get_macro_data('M0001301')  # M2 同比
print(m2)
```

**常见宏观指标**:
```python
'M0000523'  # GDP 当季同比
'M0000612'  # CPI 当月同比
'M0000613'  # PPI 当月同比
'M0001301'  # M2 同比
'M0001302'  # M1 同比
'M0001303'  # M0 同比
```

---

#### 2. get_shibor_data() - 获取 Shibor 利率

```python
# 获取 Shibor 数据
shibor = get_shibor_data('2025-12-17')
print(shibor)
```

---

#### 3. get_deposit_lending_rate() - 获取存贷款利率

```python
# 获取存款利率
rate = get_deposit_lending_rate(type='deposit')
print(rate)

# 获取贷款利率
rate = get_deposit_lending_rate(type='lending')
print(rate)
```

---

### 八、其他实用 API ⭐⭐⭐

#### 1. get_trade_days() - 获取交易日

```python
# 获取 2025 年所有交易日
days = get_trade_days(start_date='2025-01-01', 
                      end_date='2025-12-31')
print(f"2025 年共{len(days)}个交易日")

# 获取某月交易日
days = get_trade_days(start_date='2025-01-01', 
                      end_date='2025-01-31')
```

---

#### 2. get_all_securities() - 获取所有股票信息

```python
# 获取所有 A 股信息
stocks = get_all_securities(['stock'], 
                            date='2025-12-31')
print(f"共{len(stocks)}只股票")
print(stocks.head())

# 获取某行业股票
stocks = get_all_securities(types=['stock'], 
                            date='2025-12-31')
bank_stocks = stocks[stocks['industry'] == '银行']
```

---

#### 3. get_extras() - 获取额外信息

```python
# 获取股票简称
extras = get_extras('000001.XSHE', 
                    fields=['display_name'], 
                    date='2025-12-31')
print(extras)

# 获取 ST 状态
extras = get_extras('000001.XSHE', 
                    fields=['is_st'], 
                    date='2025-12-31')
```

---

#### 4. get_locked_shares() - 获取限售股

```python
# 获取限售股解禁数据
locked = get_locked_shares('000001.XSHE', 
                           start_date='2025-01-01', 
                           end_date='2025-12-31')
print(locked)
```

---

#### 5. get_report_date() - 获取财报披露日期

```python
# 获取财报披露日期
date = get_report_date(year=2025, 
                       quarter=4)  # 4 季报
print(date)
```

---

## 🎯 实战示例

### 示例 1: 获取 IPO 数据并回测

```python
from jqdatasdk import *

# 认证
auth('13606066742', 'SXM123456asd')

# 获取 2025 年 IPO 数据
ipo_stocks = get_new_stocks('2025-01', '2025-12')
print(f"2025 年共{len(ipo_stocks)}只 IPO")

# 回测每只股票上市后 5 日表现
results = []
for idx, row in ipo_stocks.iterrows():
    code = row['code']
    listing_date = row['listing_date']
    
    # 获取上市后 5 日数据
    df = get_price(code, 
                   start_date=listing_date, 
                   end_date=listing_date, 
                   count=5)
    
    if len(df) >= 5:
        return_5d = (df['close'].iloc[-1] / df['open'].iloc[0] - 1) * 100
        results.append({
            'code': code,
            'name': row['name'],
            'listing_date': listing_date,
            'return_5d': return_5d
        })

# 统计胜率
import pandas as pd
results_df = pd.DataFrame(results)
win_rate = (results_df['return_5d'] > 0).mean() * 100
avg_return = results_df['return_5d'].mean()

print(f"\n2025 年 IPO 回测结果:")
print(f"总样本：{len(results)}只")
print(f"胜率：{win_rate:.1f}%")
print(f"平均收益：{avg_return:.2f}%")
```

---

### 示例 2: 筛选低估值股票

```python
from jqdatasdk import *

auth('13606066742', 'SXM123456asd')

# 筛选 PE < 20 且 PB < 2 的股票
df = get_fundamentals(query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap
).filter(
    valuation.pe_ratio < 20,
    valuation.pb_ratio < 2,
    valuation.market_cap > 5000000000  # 市值>50 亿
))

print(f"找到{len(df)}只低估值股票:")
print(df.sort_values('pe_ratio').head(10))
```

---

### 示例 3: 获取沪深 300 成分股并分析

```python
from jqdatasdk import *

auth('13606066742', 'SXM123456asd')

# 获取沪深 300 成分股
hs300 = get_index_stocks('000300.XSHG')
print(f"沪深 300 共{len(hs300)}只成分股")

# 获取成分股的 PE 数据
df = get_fundamentals(query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio
).filter(
    valuation.code.in_(hs300)
))

print(f"\n沪深 300 估值分析:")
print(f"平均 PE: {df['pe_ratio'].mean():.2f}")
print(f"平均 PB: {df['pb_ratio'].mean():.2f}")
print(f"最低 PE: {df['pe_ratio'].min():.2f}")
print(f"最高 PE: {df['pe_ratio'].max():.2f}")
```

---

### 示例 4: 资金流向分析

```python
from jqdatasdk import *

auth('13606066742', 'SXM123456asd')

# 获取贵州茅台资金流向
flow = get_money_flow('600519.XSHG', 
                      start_date='2025-12-01', 
                      end_date='2025-12-17')

print("贵州茅台资金流向分析:")
print(f"主力净流入：{flow['net_amount_main'].sum():.2f}万")
print(f"超大单净流入：{flow['net_amount_big'].sum():.2f}万")
print(f"大单净流入：{flow['net_amount_medium'].sum():.2f}万")

# 判断主力动向
if flow['net_amount_main'].sum() > 0:
    print("结论：主力净流入，看好")
else:
    print("结论：主力净流出，看空")
```

---

## ⚠️ 注意事项

### 1. 数据范围限制

```python
# 试用账号：2024-12-10 至 2025-12-17
# 超出范围会报错

# 正确
df = get_price('000001.XSHE', 
               start_date='2025-01-01', 
               end_date='2025-12-17')

# 错误（超出范围）
df = get_price('000001.XSHE', 
               start_date='2026-01-01',  # ❌
               end_date='2026-03-19')
```

### 2. 调用频率限制

```python
# 试用账号
# - 每分钟最多 10 次请求
# - 每天最多 100 万次调用

# 避免频繁调用
import time
for code in stock_list:
    df = get_price(code)
    time.sleep(0.1)  # 添加延迟
```

### 3. 股票代码格式

```python
# 深交所股票：.XSHE 后缀
'000001.XSHE'  # 平安银行

# 上交所股票：.XSHG 后缀
'600519.XSHG'  # 贵州茅台

# 指数：.XSHG 或.XSHE
'000300.XSHG'  # 沪深 300
```

---

## 📚 学习资源

| 资源 | 链接 |
|------|------|
| **官方 API 文档** | https://www.joinquant.com/help/api/help |
| **JQData 教程** | https://www.joinquant.com/help/jqdata-tutorial |
| **常见问题** | https://www.joinquant.com/help/jqdata-faq |
| **数据规则** | https://www.joinquant.com/help/jqdata-rules |
| **量化社区** | https://www.joinquant.com/community |

---

## 🎯 总结

### 最常用 API TOP 10

| 排名 | API | 用途 | 推荐度 |
|------|-----|------|--------|
| 1 | get_price() | 获取行情 | ⭐⭐⭐⭐⭐ |
| 2 | get_fundamentals() | 获取财务数据 | ⭐⭐⭐⭐⭐ |
| 3 | get_index_stocks() | 获取指数成分股 | ⭐⭐⭐⭐ |
| 4 | get_new_stocks() | 获取 IPO 数据 | ⭐⭐⭐⭐⭐ |
| 5 | get_money_flow() | 获取资金流向 | ⭐⭐⭐⭐ |
| 6 | get_trade_days() | 获取交易日 | ⭐⭐⭐ |
| 7 | get_all_securities() | 获取股票列表 | ⭐⭐⭐ |
| 8 | get_fund_nav() | 获取基金净值 | ⭐⭐⭐ |
| 9 | get_macro_data() | 获取宏观数据 | ⭐⭐⭐ |
| 10 | get_extras() | 获取额外信息 | ⭐⭐⭐ |

---

**掌握这些 API，你就可以开始量化研究啦！** 🎉

**需要我帮你演示具体哪个 API 的用法？** 🎯
