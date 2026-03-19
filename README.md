# IPO Calendar 📅

每日自动更新 A 股、港股 IPO 上市企业数据

## 功能特点

- ✅ **自动更新**：每天 19:00 自动抓取
- ✅ **双市场覆盖**：A 股 + 港股
- ✅ **静态页面**：无需服务器，GitHub Pages 部署
- ✅ **响应式设计**：手机/电脑完美适配
- ✅ **数据校验**：智能过滤误匹配数据

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 手动测试

```bash
python main.py
```

### 3. 查看输出

- 数据文件：`data/ipo_data.json`
- 网页文件：`index.html`

## 部署到 GitHub Pages

### 1. 创建 GitHub 仓库

```bash
git init
git add .
git commit -m "Initial commit - IPO Calendar"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ipo-calendar.git
git push -u origin main
```

### 2. 启用 GitHub Pages

1. 进入仓库 Settings
2. 左侧菜单选择 Pages
3. Source 选择 `main` branch
4. 点击 Save

### 3. 访问网站

```
https://YOUR_USERNAME.github.io/ipo-calendar/
```

## 定时任务配置

### Linux/Mac (crontab)

```bash
crontab -e
# 添加以下行（每天 19 点执行）
0 19 * * * /usr/bin/python3 /path/to/ipo-calendar/main.py >> /path/to/ipo-calendar/cron.log 2>&1
```

### Windows (任务计划程序)

```powershell
schtasks /create /tn "IPO Calendar" /tr "python C:\path\to\ipo-calendar\main.py" /sc daily /st 19:00
```

### GitHub Actions（推荐）

创建 `.github/workflows/update.yml`:

```yaml
name: Update IPO Data

on:
  schedule:
    - cron: '0 11 * * *'  # UTC 11:00 = 北京时间 19:00
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run crawler
        run: python main.py
      
      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "Update IPO data $(date +%Y-%m-%d)" || exit 0
          git push
```

## 项目结构

```
ipo-calendar/
├── spiders/              # 爬虫模块
│   ├── a_stock.py       # A 股爬虫
│   ├── hk_stock.py      # 港股爬虫
│   └── __init__.py
├── generator/            # 页面生成模块
│   ├── generate.py      # HTML 生成器
│   └── __init__.py
├── data/                 # 数据存储
│   └── ipo_data.json
├── config.py             # 配置文件
├── main.py               # 主程序
├── requirements.txt      # 依赖
├── README.md             # 说明文档
└── index.html            # 生成的网页
```

## 数据源

- **A 股**：东方财富网 IPO 数据
- **港股**：东方财富网港股 IPO 数据

## 注意事项

1. **API 限制**：避免频繁请求，建议每天更新 1-2 次
2. **数据准确性**：仅供参考，请以交易所公告为准
3. **港股校验**：已添加数据校验逻辑，避免误匹配

## 技术栈

- Python 3.8+
- requests
- GitHub Pages
- HTML/CSS (响应式)

## License

MIT License

## 作者

Built with ❤️ by Henry

---

**📅 每天 19:00，准时更新明日 IPO 企业！**
