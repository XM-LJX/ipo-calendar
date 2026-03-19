# 📱 Webhook 推送配置指南

## 选择你的推送方式

### 方式 1: Server 酱（推荐 - 微信推送）⭐⭐⭐⭐⭐

**优点**：
- ✅ 直接推送到微信
- ✅ 配置简单
- ✅ 免费

**步骤**：

1. **访问 Server 酱官网**
   ```
   https://sct.ftqq.com/
   ```

2. **微信扫码登录**

3. **获取 SendKey**
   - 登录后点击左侧 "微信" 
   - 绑定你的微信
   - 复制 SendKey（类似：`SCTxxx`）

4. **填入 .env 文件**
   ```bash
   cd /Users/henry/ipo-calendar
   vim .env
   ```
   
   修改：
   ```
   SERVERCHAN_KEY=SCTxxx  # 替换为你的 SendKey
   ```

5. **测试推送**
   ```bash
   curl https://sctapi.ftqq.com/SCTxxx.send?title=测试&desp=推送成功
   ```
   
   微信会收到消息！

---

### 方式 2: 钉钉机器人 ⭐⭐⭐⭐

**优点**：
- ✅ 支持 Markdown
- ✅ 可@所有人
- ✅ 免费

**步骤**：

1. **打开钉钉**
   - 创建一个群（或选择现有群）

2. **添加机器人**
   - 群设置 → 群机器人 → 添加机器人
   - 选择 "自定义"
   - 点击 "添加"

3. **配置机器人**
   - 机器人名称：`IPO Calendar`
   - 头像：（可选）
   - ✅ 勾选 "自定义关键词"
   - 关键词：`IPO`
   - 点击 "完成"

4. **复制 Webhook**
   ```
   https://oapi.dingtalk.com/robot/send?access_token=xxx
   ```

5. **填入 .env 文件**
   ```bash
   vim .env
   ```
   
   修改：
   ```
   DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
   ```
   
   其他两个留空或删除

6. **测试推送**
   ```bash
   curl 'https://oapi.dingtalk.com/robot/send?access_token=xxx' \
   -H 'Content-Type: application/json' \
   -d '{
     "msgtype": "text",
     "text": {
       "content": "测试推送"
     }
   }'
   ```

---

### 方式 3: 企业微信机器人 ⭐⭐⭐⭐

**优点**：
- ✅ 支持 Markdown
- ✅ 企业微信用户
- ✅ 免费

**步骤**：

1. **打开企业微信**
   - 创建一个群

2. **添加机器人**
   - 群设置 → 群机器人 → 添加
   - 点击 "新建"

3. **配置机器人**
   - 名称：`IPO Calendar`
   - 点击 "添加"

4. **复制 Webhook**
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
   ```

5. **填入 .env 文件**
   ```bash
   vim .env
   ```
   
   修改：
   ```
   WECHAT_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
   ```

6. **测试推送**
   ```bash
   curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx' \
   -H 'Content-Type: application/json' \
   -d '{
     "msgtype": "text",
     "text": {
       "content": "测试推送"
     }
   }'
   ```

---

## 配置完成后的 .env 文件

**示例（使用 Server 酱）**：
```
# 钉钉机器人 Webhook（不使用则留空）
DINGTALK_WEBHOOK=

# 企业微信机器人 Webhook（不使用则留空）
WECHAT_WEBHOOK=

# Server 酱 SendKey（填入你的）
SERVERCHAN_KEY=SCTxxx
```

**示例（使用钉钉）**：
```
# 钉钉机器人 Webhook（填入你的）
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx

# 企业微信机器人 Webhook（不使用则留空）
WECHAT_WEBHOOK=

# Server 酱 SendKey（不使用则留空）
SERVERCHAN_KEY=
```

---

## 测试推送

### 方法 1: 运行主程序

```bash
cd /Users/henry/ipo-calendar
venv/bin/python main.py
```

如果有符合条件的亮点数据，会自动推送！

### 方法 2: 手动测试

```bash
cd /Users/henry/ipo-calendar
venv/bin/python -c "from utils.webhook import send_webhook; send_webhook(['🔥 测试推送', 'IPO Calendar 已就绪'])"
```

---

## 推送规则

**触发条件**（满足任一即推送）：
- 暗盘涨幅 ≥ 10%
- 超额认购 ≥ 100 倍  
- 知名基石投资者

**推送时间**：
- 每天 19:00（GitHub Actions 自动）
- 手动运行 `python main.py` 时

---

## 常见问题

### Q: 收不到推送？

**检查**：
1. .env 文件是否正确配置
2. Webhook URL 是否正确
3. 是否有符合条件的数据
4. 查看运行日志是否有错误

### Q: 可以配置多个推送？

**可以**！在 .env 中同时配置多个：
```
DINGTALK_WEBHOOK=xxx
SERVERCHAN_KEY=xxx
```

会同时推送到钉钉和微信！

### Q: 推送太频繁怎么办？

**修改推送阈值**：

编辑 `utils/webhook.py`：
```python
if pct >= 10:  # 改为 20 表示只推送涨幅>20%
```

---

## 推荐配置

**个人用户**：Server 酱（微信推送）
- 配置简单
- 直接推送到微信
- 不会错过重要信息

**团队用户**：钉钉/企业微信
- 可@所有人
- 团队共享信息
- 支持更丰富的格式

---

**配置完成后告诉我，我帮你测试！** 🎯
