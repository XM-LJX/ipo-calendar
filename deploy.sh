#!/bin/bash
# IPO Calendar 一键推送脚本

echo "🚀 开始推送到 GitHub..."
echo ""
echo "GitHub 用户名：XM-LJX"
echo "仓库地址：https://github.com/XM-LJX/ipo-calendar"
echo ""

# 检查 Git 配置
if ! git config user.name > /dev/null 2>&1; then
    echo "⚠️  未配置 Git 用户信息"
    read -p "请输入你的姓名：" git_name
    read -p "请输入你的邮箱：" git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
fi

# 检查 remote
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  未配置 remote"
    git remote add origin https://github.com/XM-LJX/ipo-calendar.git
fi

# 推送
echo ""
echo "📤 推送到 GitHub..."
echo "需要输入 GitHub 认证信息"
echo "Username: XM-LJX"
echo "Password: 使用 Personal Access Token (不是登录密码)"
echo ""
echo "获取 Token: https://github.com/settings/tokens"
echo ""

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "📱 下一步："
    echo "1. 访问：https://github.com/XM-LJX/ipo-calendar"
    echo "2. Settings → Pages"
    echo "3. Source: 选择 main branch"
    echo "4. Save"
    echo ""
    echo "🌐 网站地址："
    echo "https://XM-LJX.github.io/ipo-calendar/"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能原因："
    echo "1. 仓库不存在 → 先在 GitHub 创建仓库"
    echo "2. 认证失败 → 使用 Personal Access Token"
    echo "3. 权限不足 → 检查 Token 权限"
    echo ""
    echo "详细指南：查看 PUSH_TO_GITHUB.md"
fi
