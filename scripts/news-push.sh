#!/bin/bash
# 新闻推送脚本 - 财经 + 科技 + 国内外大事件
# 推送目标：YKK 家庭议事群

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$WORKSPACE_DIR/logs/news-push.log"

# 创建日志目录
mkdir -p "$WORKSPACE_DIR/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "开始执行新闻推送任务..."

# 使用 OpenClaw 发送消息到飞书群
# 需要获取 YKK 家庭议事群的 chat_id
# 这里使用 message 工具推送

# 获取新闻内容（使用 web_search 搜索最新新闻）
# 由于 shell 脚本无法直接调用 OpenClaw 工具，我们需要通过 sessions_spawn 或 message 来推送

# 方法：创建一个临时的任务描述，通过 OpenClaw 的消息系统推送
# 这里我们调用一个 Node.js 脚本来处理

node "$SCRIPT_DIR/news-fetcher.js"

if [ $? -eq 0 ]; then
    log "新闻推送完成"
else
    log "新闻推送失败"
    exit 1
fi
