#!/bin/bash
# Home Assistant Docker 安装脚本（macOS）
# wrui 专用版本 - 2026-03-05

set -e

echo "🏠 开始安装 Home Assistant..."
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装！请先安装 Docker Desktop for Mac"
    echo "下载地址：https://www.docker.com/products/docker-desktop/"
    exit 1
fi

echo "✅ Docker 已安装：$(docker --version)"
echo ""

# 创建配置目录
CONFIG_DIR="$HOME/homeassistant"
echo "📁 创建配置目录：$CONFIG_DIR"
mkdir -p "$CONFIG_DIR"

# 启动 Home Assistant 容器
echo "🐳 启动 Home Assistant 容器..."
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v "$CONFIG_DIR:/config" \
  -v /etc/localtime:/etc/localtime:ro \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable

echo ""
echo "✅ Home Assistant 启动成功！"
echo ""
echo "📱 访问地址：http://$(hostname -I | awk '{print $1}'):8123"
echo "   或者：http://localhost:8123"
echo ""
echo "📝 常用命令："
echo "   查看状态：docker ps | grep homeassistant"
echo "   查看日志：docker logs homeassistant"
echo "   重启：docker restart homeassistant"
echo "   停止：docker stop homeassistant"
echo "   启动：docker start homeassistant"
echo ""
echo "🔧 下一步："
echo "   1. 浏览器打开 http://localhost:8123"
echo "   2. 创建管理员账号"
echo "   3. 在配置中添加米家集成（Xiaomi Miio）"
echo ""
echo "🎉 安装完成！"
