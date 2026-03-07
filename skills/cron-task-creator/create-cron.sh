#!/bin/bash
# Cron 任务创建助手
# 基于今天的实战经验，避免踩坑

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_step() {
    echo -e "${BLUE}>>> $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查依赖
check_dependencies() {
    print_step "检查依赖..."
    
    if ! command -v openclaw &> /dev/null; then
        print_error "OpenClaw 未安装，请先安装：npm install -g openclaw"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_warning "Python3 未安装，某些功能可能不可用"
    fi
    
    print_success "依赖检查完成"
}

# 引导问题
ask_question() {
    echo ""
    print_step "$1"
    read -p "> " answer
    echo "$answer"
}

# 验证 Cron 表达式
validate_cron() {
    local cron="$1"
    
    # 简单验证
    if [[ ! "$cron" =~ ^[0-9\*\/\,\-]+[[:space:]] ]]; then
        print_error "Cron 表达式格式错误"
        return 1
    fi
    
    print_success "Cron 表达式格式正确"
    return 0
}

# 创建记忆文件
create_memory() {
    local task_name="$1"
    local memory_file="$HOME/.openclaw/workspace/MEMORY.md"
    
    print_step "更新记忆文件..."
    
    if [ ! -f "$memory_file" ]; then
        cat > "$memory_file" << EOF
# 长期记忆

## 任务历史
- $(date +%Y-%m-%d): 创建 $task_name 任务

## 推送偏好
- 时间：每天 08:00
- 格式：简洁列表
- 目标：待配置

## 已读内容（避免重复）
EOF
        print_success "记忆文件已创建"
    else
        echo "- $(date +%Y-%m-%d): 创建 $task_name 任务" >> "$memory_file"
        print_success "记忆文件已更新"
    fi
}

# 创建心跳配置
create_heartbeat() {
    local task_name="$1"
    local heartbeat_file="$HOME/.openclaw/workspace/HEARTBEAT.md"
    
    print_step "创建心跳配置..."
    
    cat >> "$heartbeat_file" << EOF

## $task_name 检查
- [ ] 任务是否正常执行
- [ ] API Key 是否有效
- [ ] 网络连接是否正常
EOF
    
    print_success "心跳配置已创建"
}

# 主流程
main() {
    echo ""
    echo "========================================"
    echo "   🦞 OpenClaw Cron 任务创建助手"
    echo "   基于 2026-03-05 实战经验"
    echo "========================================"
    echo ""
    
    # 检查依赖
    check_dependencies
    
    # 引导问题
    TASK_NAME=$(ask_question "任务名称？（建议格式：功能 - 目标 - 频率）")
    
    echo ""
    echo "执行频率选项："
    echo "1. 每小时 (0 * * * *)"
    echo "2. 每天早上 8 点 (0 8 * * *)"
    echo "3. 每天多个时间 (0 8,12,18 * * *)"
    echo "4. 每 2 小时 (0 */2 * * *)"
    echo "5. 自定义"
    
    read -p "请选择 (1-5): " freq_choice
    
    case $freq_choice in
        1) CRON_EXPR="0 * * * *" ;;
        2) CRON_EXPR="0 8 * * *" ;;
        3) CRON_EXPR="0 8,12,18 * * *" ;;
        4) CRON_EXPR="0 */2 * * *" ;;
        5) CRON_EXPR=$(ask_question "请输入 Cron 表达式") ;;
        *) print_error "无效选择"; exit 1 ;;
    esac
    
    validate_cron "$CRON_EXPR" || exit 1
    
    TASK_DESC=$(ask_question "任务具体做什么？（详细描述）")
    
    PUSH_TARGET=$(ask_question "推送目标？（飞书 ID: oc_xxx 或 ou_xxx）")
    
    read -p "是否需要心跳检查？(y/n): " need_heartbeat
    need_heartbeat=$(echo "$need_heartbeat" | tr '[:upper:]' '[:lower:]')
    
    # 显示配置
    echo ""
    echo "========================================"
    echo "   配置确认"
    echo "========================================"
    echo ""
    echo "任务名称：$TASK_NAME"
    echo "执行频率：$CRON_EXPR"
    echo "任务描述：$TASK_DESC"
    echo "推送目标：$PUSH_TARGET"
    echo "心跳检查：$need_heartbeat"
    echo ""
    
    read -p "是否创建此任务？(y/n): " confirm
    confirm=$(echo "$confirm" | tr '[:upper:]' '[:lower:]')
    
    if [ "$confirm" != "y" ]; then
        print_warning "已取消"
        exit 0
    fi
    
    # 创建任务
    print_step "创建定时任务..."
    
    openclaw cron add \
        --name "$TASK_NAME" \
        --cron "$CRON_EXPR" \
        --message "$TASK_DESC" \
        --session "isolated" \
        --description "自动创建于 $(date +%Y-%m-%d)"
    
    TASK_ID=$(openclaw cron list | grep "$TASK_NAME" | awk '{print $1}')
    
    if [ -n "$TASK_ID" ]; then
        print_success "任务创建成功：$TASK_ID"
        
        # 配置推送目标
        print_step "配置推送目标..."
        openclaw cron edit "$TASK_ID" --to "$PUSH_TARGET"
        print_success "推送目标已配置"
    else
        print_error "任务创建失败"
        exit 1
    fi
    
    # 创建记忆文件
    if [ "$need_heartbeat" == "y" ]; then
        create_memory "$TASK_NAME"
        create_heartbeat "$TASK_NAME"
    fi
    
    # 验证
    echo ""
    print_step "验证配置..."
    echo ""
    echo "运行以下命令验证："
    echo "  openclaw cron list              # 查看任务列表"
    echo "  openclaw cron status            # 查看状态"
    echo "  openclaw cron run $TASK_ID      # 手动测试"
    echo "  openclaw cron runs --id $TASK_ID # 查看执行历史"
    echo ""
    
    read -p "是否立即测试运行？(y/n): " test_now
    test_now=$(echo "$test_now" | tr '[:upper:]' '[:lower:]')
    
    if [ "$test_now" == "y" ]; then
        print_step "运行测试..."
        openclaw cron run "$TASK_ID"
        print_success "测试完成，请检查推送结果"
    fi
    
    echo ""
    print_success "任务创建完成！🎉"
    echo ""
    echo "下次执行时间：查看 openclaw cron list"
    echo "文档位置：~/.openclaw/workspace/docs/cron-task-creator.md"
    echo ""
}

# 运行
main
