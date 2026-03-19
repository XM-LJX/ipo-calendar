# 🚀 推送到 GitHub - 快速指南

**GitHub 用户名**: XM-LJX  
**仓库地址**: https://github.com/XM-LJX/ipo-calendar

---

## 方法一：使用 GitHub Token（推荐）⭐⭐⭐⭐⭐

### 1. 创建 Personal Access Token

访问：https://github.com/settings/tokens/new

**配置**:
- Note: `ipo-calendar-push`
- Expiration: `No expiration` (或选择 1 年)
- Scopes: 勾选 `repo` (完整控制)

点击 **Generate token**

**复制 Token** (只显示一次！): `ghp_xxxxxxxxxxxx`

---

### 2. 推送代码

```bash
cd /Users/henry/ipo-calendar

# 使用 Token 推送
git remote add origin https://ghp_xxxxxxxxxxxx@github.com/XM-LJX/ipo-calendar.git
git branch -M main
git push -u origin main
```

**替换**: `ghp_xxxxxxxxxxxx` 为你的 Token

---

## 方法二：使用 GitHub Desktop（最简单）⭐⭐⭐⭐⭐

### 1. 下载 GitHub Desktop

访问：https://desktop.github.com/

下载安装并登录 GitHub 账号

---

### 2. 添加项目

1. 打开 GitHub Desktop
2. File → Add Local Repository
3. 选择：`/Users/henry/ipo-calendar`
4. 点击 **Add repository**

---

### 3. 发布到 GitHub

1. 点击右上角 **Publish repository**
2. Name: `ipo-calendar`
3. ✅ 勾选 "Keep this code private" (可选)
4. 点击 **Publish repository**

完成！🎉

---

## 方法三：使用 SSH（一劳永逸）⭐⭐⭐⭐

### 1. 生成 SSH Key

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
# 一路回车
```

### 2. 添加 SSH Key 到 GitHub

```bash
cat ~/.ssh/id_ed25519.pub
# 复制输出内容
```

访问：https://github.com/settings/keys/new

粘贴公钥内容，点击 **Add SSH key**

---

### 3. 使用 SSH 推送

```bash
cd /Users/henry/ipo-calendar

# 删除之前的 remote（如果有）
git remote remove origin

# 添加 SSH remote
git remote add origin git@github.com:XM-LJX/ipo-calendar.git

# 推送
git push -u origin main
```

---

## 方法四：直接在 GitHub 创建仓库后推送 ⭐⭐⭐

### 1. 创建仓库

访问：https://github.com/new

**填写**:
- Repository name: `ipo-calendar`
- Description: `每日更新 A 股、港股 IPO 上市企业数据`
- ✅ Public
- ❌ 不要勾选 "Add a README file"

点击 **Create repository**

---

### 2. 推送代码

复制页面显示的命令，依次执行：

```bash
cd /Users/henry/ipo-calendar

git remote add origin https://github.com/XM-LJX/ipo-calendar.git
git branch -M main
git push -u origin main
```

**会提示输入 GitHub 账号密码**:
- Username: `XM-LJX`
- Password: 使用 Personal Access Token（不是登录密码）

---

## ✅ 推送成功后

### 1. 启用 GitHub Pages

1. 进入仓库：https://github.com/XM-LJX/ipo-calendar
2. Settings → Pages
3. Source: 选择 `main` branch
4. 点击 **Save**

### 2. 访问网站

等待 1-2 分钟后访问：

```
https://XM-LJX.github.io/ipo-calendar/
```

---

## 🎯 推荐方案

**最简单**: GitHub Desktop（方法二）  
**最推荐**: Personal Access Token（方法一）  
**最方便**: SSH Key（方法三，一次配置永久使用）

---

## 📱 后续自动更新

推送成功后，GitHub Actions 会自动运行：

1. 进入仓库 → Actions 标签
2. 查看 **Update IPO Data** workflow
3. 每天 19:00 自动执行
4. 可手动触发：Run workflow

---

## ❓ 遇到问题？

### 问题 1: Authentication failed

**解决**: 使用 Personal Access Token，不是登录密码

### 问题 2: Repository not found

**解决**: 确认已在 GitHub 创建仓库

### 问题 3: Permission denied

**解决**: 检查 Token 是否有 repo 权限

---

**需要帮助？** 把错误信息发给我！🎯
