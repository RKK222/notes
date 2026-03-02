#!/bin/bash
# 自动推送脚本 - 由 LitteleAurora 使用

cd ~/.openclaw/workspace/notes

# 检查是否有变更
if [ -z "$(git status --porcelain)" ]; then
    echo "没有变更需要推送"
    exit 0
fi

# 添加、提交、推送
git add .
git commit -m "自动更新 - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo "推送完成！"
