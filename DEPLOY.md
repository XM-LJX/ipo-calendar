# 🚀 IPO Calendar 部署指南

## ✅ 项目已创建完成！

**项目位置**: `/Users/henry/ipo-calendar/`

---

## 📋 下一步：推送到 GitHub

### 1. 创建 GitHub 仓库

打开浏览器访问：https://github.com/new

**仓库信息**:
- Repository name: `ipo-calendar`
- Description: `每日更新 A 股、港股 IPO 上市企业数据`
- Visibility: **Public** (GitHub Pages 需要公开仓库)
- ❌ 不要勾选 "Add a README file"

点击 **Create repository**

---

### 2. 推送代码到 GitHub

在终端执行以下命令：

```bash
cd /Users/henry/ipo-calendar

# 配置 Git 用户信息（首次使用需要）
git config --global user.name "Henry"
git config --global user.email "your-email@example.com"

# 推送到 GitHub
git remote add origin https://github.com/YOUR_USERNAME/ipo-calendar.git
git branch -M main
git push -u origin main
```

**替换**:
- `YOUR_USERNAME` → 你的 GitHub 用户名
- `your-email@example.com` → 你的邮箱

---

### 3. 启用 GitHub Pages

1. 进入你的仓库页面：`https://github.com/YOUR_USERNAME/ipo-calendar`
2. 点击 **Settings** (设置)
3. 左侧菜单选择 **Pages**
4. **Build and deployment** 部分:
   - Source: 选择 `Deploy from a branch`
   - Branch: 选择 `main`，文件夹选择 `/ (root)`
5. 点击 **Save**

---

### 4. 等待部署完成

等待 1-2 分钟，GitHub 会自动部署你的网站。

**访问地址**:
```
https://YOUR_USERNAME.github.io/ipo-calendar/
```

---

## ⚙️ GitHub Actions 自动更新

### 已配置

项目已包含 GitHub Actions 配置文件 (`.github/workflows/update.yml`)

**自动更新时间**:
- 每天北京时间 19:00 (UTC 11:00)
- 自动抓取数据并提交更新

### 手动触发

如需手动更新：

1. 进入仓库页面
2. 点击 **Actions** 标签
3. 选择 **Update IPO Data** workflow
4. 点击 **Run workflow**
5. 等待执行完成

---

## 📊 测试运行

### 本地测试

```bash
cd /Users/henry/ipo-calendar
venv/bin/python main.py
```

### 查看输出

- **数据文件**: `data/ipo_data.json`
- **网页文件**: `index.html`

直接在浏览器打开 `index.html` 查看效果！

---

## 🔧 常见问题

### Q1: GitHub Pages 显示 404？

**解决**:
- 等待 2-3 分钟
- 检查仓库是否为 Public
- 检查 Settings → Pages 配置是否正确

### Q2: Actions 执行失败？

**检查**:
1. 进入 Actions 标签查看日志
2. 确认 `requirements.txt` 正确
3. 检查 API 是否可访问

### Q3: 数据为空？

**原因**:
- 次日确实没有 IPO 企业
- API 暂时不可用

**解决**:
- 手动运行 `python main.py` 查看错误信息
- 检查网络连接

---

## 📱 自定义域名（可选）

如需使用自定义域名：

1. 在域名服务商添加 CNAME 记录：
   ```
   your-domain.com → YOUR_USERNAME.github.io
   ```

2. 在仓库 Settings → Pages → Custom domain 输入你的域名

3. 创建 `CNAME` 文件（仓库根目录）：
   ```
   your-domain.com
   ```

---

## 🎉 完成！

现在你有一个自动更新的 IPO 日历网站了！

**每日自动更新**:
- ⏰ 每天 19:00 自动抓取
- 📊 A 股 + 港股全覆盖
- 🌐 自动部署到 GitHub Pages

**访问你的网站**:
```
https://YOUR_USERNAME.github.io/ipo-calendar/
```

---

**需要帮助？**

遇到问题随时问我！🎯
