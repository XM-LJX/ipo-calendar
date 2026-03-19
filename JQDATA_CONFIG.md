# 🎉 聚宽 JQData 配置完成！

## ✅ 账号信息

| 项目 | 内容 |
|------|------|
| **账号** | 13606066742 |
| **密码** | SXM123456asd |
| **有效期** | 2026-06-21（3 个月试用） |
| **数据范围** | 前 15 个月~前 3 个月 |
| **每日流量** | 100 万条 |
| **连接数** | 1 个 |

---

## 📁 已配置文件

| 文件 | 用途 |
|------|------|
| `.env` | 存储 JQData 账号密码 |
| `data/jqdata_client.py` | JQData 数据获取模块 |

---

## 🚀 快速使用

### 方式 1: 测试连接

```bash
cd /Users/henry/ipo-calendar
venv/bin/python data/jqdata_client.py
```

**预期输出**:
```
============================================================
🧪 JQData 连接测试
============================================================
✅ JQData 认证成功！账号：13606066742
📊 账号有效期：2026-06-21
📊 每日流量：1000000

【测试 1】获取平安银行行情数据
✅ 获取 000001.XSHE 行情数据成功，共 14 条
            open   close    high     low     volume
2026-03-19  10.50  10.85  10.92  10.45  1234567

【测试 2】获取 2026 年 IPO 数据
✅ 获取 IPO 数据成功，共 XX 只

【测试 3】获取沪深 300 成分股
✅ 获取 000300.XSHG 成分股成功，共 300 只

============================================================
✅ JQData 测试完成！
============================================================
```

---

### 方式 2: 在策略中使用

```python
from data.jqdata_client import JQDataClient

# 初始化客户端
client = JQDataClient()

# 获取股票行情
df = client.get_stock_price('000001.XSHE', 
                             start_date='2026-01-01', 
                             end_date='2026-03-19')

# 获取 IPO 数据
ipo_df = client.get_new_stocks('2026-01', '2026-03')

# 获取财务数据
from jqdatasdk import query, valuation
finance_df = client.get_fundamentals(
    query(valuation.code, valuation.pe_ratio)
    .filter(valuation.code.in_(['000001.XSHE', '000002.XSHE']))
)
```

---

## 📊 可用数据

| 数据类型 | API | 示例 |
|---------|-----|------|
| **股票行情** | `get_stock_price()` | 日线/分钟线 |
| **IPO 数据** | `get_new_stocks()` | 新股发行日历 |
| **指数成分股** | `get_index_stocks()` | 沪深 300 成分股 |
| **财务数据** | `get_fundamentals()` | PE/PB/营收 |
| **资金流向** | `get_money_flow()` | 主力/散户资金 |

---

## ⚠️ 注意事项

### 1. 安装依赖

如果还没安装 jqdatasdk：
```bash
cd /Users/henry/ipo-calendar
venv/bin/pip install jqdatasdk
```

如果遇到 `thriftpy2` 安装错误：
```bash
venv/bin/pip install thriftpy2==0.4.20
venv/bin/pip install jqdatasdk
```

### 2. 试用限制

| 限制 | 试用版 | 正式版 |
|------|--------|--------|
| 数据范围 | 前 15 个月~前 3 个月 | 2005 年至今 |
| 每日流量 | 100 万条 | 2 亿条 |
| 连接数 | 1 个 | 3 个 |
| 有效期 | 3 个月 | 12 个月 |

### 3. 账号安全

```
⚠️ 不要共享账号密码
⚠️ 不要多账号同时使用
⚠️ 违反保密协议会封号
```

---

## 🎯 下一步

### 选项 A: 测试连接
```bash
venv/bin/python data/jqdata_client.py
```

### 选项 B: 集成到 IPO 策略
```python
# 在 main.py 中添加
from data.jqdata_client import JQDataClient

client = JQDataClient()
ipo_data = client.get_new_stocks('2026-03')
```

### 选项 C: 回测历史 IPO 表现
```python
# 获取 2025 年 IPO 数据
ipo_2025 = client.get_new_stocks('2025-01', '2025-12')

# 获取每只股票上市后 5 日表现
for stock in ipo_2025:
    code = stock['code']
    listing_date = stock['listing_date']
    
    # 获取上市后 5 日数据
    df = client.get_stock_price(code, 
                                 start_date=listing_date, 
                                 end_date=listing_date + '5 days')
    
    # 计算收益率
    return_5d = (df['close'].iloc[-1] / df['open'].iloc[0] - 1) * 100
```

---

## 📚 学习资源

| 资源 | 链接 |
|------|------|
| **JQData 文档** | https://www.joinquant.com/help/api |
| **数据规则** | https://www.joinquant.com/help/jqdata-rules |
| **安装教程** | https://www.joinquant.com/help/jqdata-install |
| **常见问题** | https://www.joinquant.com/help/jqdata-faq |

---

**配置完成！现在可以开始使用 JQData 获取金融数据了！** 🎉

**运行测试**：
```bash
cd /Users/henry/ipo-calendar
venv/bin/python data/jqdata_client.py
```
