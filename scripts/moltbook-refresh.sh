#!/bin/bash
# Moltbook 会话保持脚本 - 每小时刷新一次页面
# 防止登录会话过期

echo "🦞 [$(date '+%Y-%m-%d %H:%M:%S')] 刷新 Moltbook 会话..."

# 使用 curl 访问 moltbook，保持 Cookie
curl -s -o /dev/null -w "%{http_code}" \
  --cookie-jar /tmp/moltbook-cookies.txt \
  --cookie /tmp/moltbook-cookies.txt \
  https://www.moltbook.com/

echo "✅ Moltbook 刷新完成"
