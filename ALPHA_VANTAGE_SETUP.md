# 🔑 Alpha Vantage API 配置指南

## 什么是 Alpha Vantage？

**Alpha Vantage** 是免费的金融数据 API 提供商，提供：
- ✅ 股票实时/历史行情
- ✅ 技术指标
- ✅ 外汇、加密货币
- ✅ 基本面数据

**免费额度**：
- 每天 500 次请求
- 每分钟 5 次请求

---

## 获取 API Key

### 步骤 1: 访问官网

```
https://www.alphavantage.co/support/#api-key
```

### 步骤 2: 填写申请表

| 字段 | 填写内容 |
|------|---------|
| Name | 你的名字 |
| Email | 你的邮箱 |
| Company | 个人/公司名 |
| Country | China |

### 步骤 3: 接收 API Key

- 提交后**立即显示**在页面
- 同时发送到邮箱
- 格式：`XXXXXXXXXXXXXXXXXXXX`

---

## 配置到项目

### 1. 复制 .env 文件

```bash
cd /Users/henry/ipo-calendar
cp .env.example .env
```

### 2. 编辑 .env

```bash
vim .env
```

### 3. 填入 API Key

```
ALPHA_VANTAGE_KEY=你的 API Key
```

---

## 测试 API

```bash
# 测试获取苹果股价
curl "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=你的 API Key"
```

**返回示例**：
```json
{
  "Time Series (Daily)": {
    "2026-03-19": {
      "1. open": "170.00",
      "2. high": "172.50",
      "3. low": "169.50",
      "4. close": "171.80"
    }
  }
}
```

---

## 在项目中的用途

### 1. 保荐人历史胜率计算

```python
from utils.alpha_vantage import AlphaVantage

av = AlphaVantage()

# 计算摩根士丹利保荐的股票表现
sample_stocks = [
    {"symbol": "9999.HK", "listing_date": "2026-01-15"},
    {"symbol": "8888.HK", "listing_date": "2026-02-20"}
]

stats = av.get_sponsor_performance("摩根士丹利", sample_stocks)
print(f"胜率：{stats['win_rate']}")
print(f"平均收益：{stats['avg_return']}")
```

### 2. IPO 回测功能

```python
# 回测 2026 年所有港股 IPO
ipo_list = [...]  # IPO 列表
results = av.backtest_ipo(ipo_list, hold_days=5)

print(f"总样本：{results['total']}")
print(f"胜率：{results['wins']/results['total']*100:.1f}%")
print(f"平均收益：{results['avg_return']:.2f}%")
print(f"最佳：{results['best']}")
print(f"最差：{results['worst']}")
```

---

## 局限性

### ❌ 不适合的数据

| 数据类型 | 原因 | 替代方案 |
|---------|------|---------|
| A 股数据 | 覆盖不全 | 东方财富 API |
| 港股 IPO 数据 | 无发行信息 | 港交所披露易 |
| 暗盘数据 | 不提供 | 富途/辉立 API |
| 认购倍数 | 不提供 | 港交所官方 |

### ✅ 适合的数据

| 数据类型 | 用途 |
|---------|------|
| 美股历史行情 | 保荐人胜率计算 |
| 港股历史行情 | IPO 回测 |
| 技术指标 | 市场分析 |
| 实时股价 | 估值分析 |

---

## 推荐的数据源组合

| 功能 | 数据源 |
|------|--------|
| **IPO 基本信息** | 东方财富 + 港交所 |
| **暗盘数据** | 富途牛牛 API |
| **认购数据** | 港交所披露易 |
| **历史回测** | Alpha Vantage ⭐ |
| **保荐人胜率** | Alpha Vantage ⭐ |
| **实时股价** | Alpha Vantage |

---

## 免费 API 对比

| API | 免费额度 | 数据质量 | 推荐度 |
|-----|---------|---------|--------|
| **Alpha Vantage** | 500 次/天 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Yahoo Finance** | 无限制 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **IEX Cloud** | 5 万次/月 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Polygon.io** | 5000 次/月 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 升级建议

### 如果 Alpha Vantage 不够用

**方案 1: 多个 API 轮换**
```python
api_keys = ["key1", "key2", "key3"]
api_key = random.choice(api_keys)
```

**方案 2: 付费升级**
- Alpha Vantage Premium: $49.99/月
- 无限次请求
- 更多数据字段

**方案 3: 自建数据源**
- 爬取 Yahoo Finance
- 使用聚宽/优矿（国内）

---

## 快速开始

```bash
# 1. 获取 API Key
https://www.alphavantage.co/support/#api-key

# 2. 配置 .env
vim .env
ALPHA_VANTAGE_KEY=你的 Key

# 3. 测试
cd /Users/henry/ipo-calendar
venv/bin/python -c "from utils.alpha_vantage import AlphaVantage; av = AlphaVantage(); print(av.get_daily('AAPL'))"
```

---

**配置完成后运行回测功能！** 🎯

```bash
venv/bin/python main.py --backtest 2026-01
```
