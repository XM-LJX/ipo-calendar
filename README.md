# IPO Calendar v2.0 📅

**火控瞄准系统** - 专业级 IPO 打新分析工具

## 🚀 v2.0 新增功能

### 1. 🔥 港股暗盘交易数据
- **辉立证券/富途牛牛**暗盘收盘价
- **暗盘涨跌幅**（标红/标绿显示）
- 上市前一日 16:15-18:30 数据

### 2. 📊 情绪温度计
- **超额认购倍数**（>50 倍显示🔥热门）
- **中签率**百分比
- 认购不足显示⚠️警告

### 3. 💎 基石投资者与保荐人
- **基石投资者**名单（高瓴、红杉等）
- **保荐人历史胜率**评级
- 知名投行⭐⭐⭐⭐⭐评级

### 4. 📱 Webhook 消息推送
- **钉钉机器人**
- **企业微信机器人**
- **Server 酱**微信推送

### 5. 📅 日期选择器
- 前后 7 天日期切换
- 查看历史 IPO 数据

---

## 快速开始

### 安装依赖

```bash
cd /Users/henry/ipo-calendar
venv/bin/pip install -r requirements.txt
```

### 配置 Webhook（可选）

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑 .env，填入你的 Webhook URL
vim .env
```

### 运行

```bash
# 查看明日数据
venv/bin/python main.py

# 查看指定日期
venv/bin/python main.py --date 2026-03-20
```

---

## 数据说明

### 暗盘数据
- **更新时间**：上市前一日 18:30 后
- **数据来源**：辉立证券、富途牛牛
- **意义**：暗盘涨跌≈明日开盘预演

### 认购数据
- **超额认购倍数**：越高越热门
- **中签率**：越低越难中
- **热门标志**：≥50 倍显示🔥

### 保荐人评级
| 评级 | 胜率 | 保荐人 |
|------|------|--------|
| ⭐⭐⭐⭐⭐ | 75%+ | 摩根士丹利、高盛、中金等 |
| ⭐⭐⭐ | 50%+ | 其他投行 |

---

## Webhook 配置

### 钉钉机器人

1. 钉钉群 → 群设置 → 智能助手 → 添加机器人
2. 选择"自定义"
3. 复制 Webhook 地址
4. `.env` 文件填入：
   ```
   DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
   ```

### 企业微信机器人

1. 企业微信群 → 群设置 → 群机器人
2. 添加机器人
3. 复制 Webhook 地址
4. `.env` 文件填入：
   ```
   WECHAT_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
   ```

### Server 酱

1. 访问：https://sct.ftqq.com/
2. 获取 SendKey
3. `.env` 文件填入：
   ```
   SERVERCHAN_KEY=你的 SendKey
   ```

---

## 推送规则

**触发条件**（满足任一即推送）：
- 暗盘涨幅 ≥ 10%
- 超额认购 ≥ 100 倍
- 知名基石投资者

**推送内容**：
```
📅 IPO 日历 - 明日打新提醒

🔥 某某公司 (09999.HK) 暗盘大涨 +15.32%
🔥 某某公司 超额认购 150 倍
💎 某某公司 获高瓴资本基石投资

📊 详细：https://XM-LJX.github.io/ipo-calendar/
```

---

## 项目结构

```
ipo-calendar/
├── spiders/              # 爬虫模块
│   ├── a_stock.py       # A 股 IPO
│   ├── hk_stock.py      # 港股 IPO
│   ├── hk_darkpool.py   # 港股暗盘 ⭐
│   ├── ipo_subscription.py  # 认购数据 ⭐
│   └── ipo_cornerstone.py   # 基石投资者 ⭐
├── generator/            # 页面生成
│   └── generate.py      # HTML 生成（增强版）
├── utils/                # 工具模块
│   └── webhook.py       # Webhook 推送 ⭐
├── data/                 # 数据存储
│   └── ipo_data.json
├── .env.example          # 环境变量示例
├── config.py             # 配置
├── main.py               # 主程序
└── README.md             # 说明文档
```

---

## 高级用法

### 查看历史数据

```bash
# 查看 7 天前
venv/bin/python main.py --date 2026-03-13

# 查看 3 天后
venv/bin/python main.py --date 2026-03-22
```

### 自定义推送阈值

编辑 `utils/webhook.py`：
```python
if pct >= 10:  # 改为 20 表示只推送涨幅>20%
```

---

## 数据源

| 数据类型 | 数据源 |
|---------|--------|
| IPO 基本信息 | 东方财富网 |
| 暗盘数据 | 辉立证券、富途牛牛 |
| 认购数据 | 东方财富网 |
| 基石投资者 | 港交所披露易 |

---

## 部署

### GitHub Actions（自动更新）

已配置每天 19:00 自动更新：
```yaml
name: Update IPO Data
on:
  schedule:
    - cron: '0 11 * * *'  # 北京时间 19:00
```

### 本地定时任务

```bash
# Crontab
0 19 * * * cd /Users/henry/ipo-calendar && venv/bin/python main.py
```

---

## License

MIT License

---

**📅 每天 19:00，准时更新明日 IPO 企业！**

**🔥 暗盘数据 + 认购热度 + 基石背书 = 打新神器！**
