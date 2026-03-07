# Cron 任务创建技能

**技能名称**: `cron-task-creator`  
**版本**: 1.0  
**创建时间**: 2026-03-05  
**作者**: OpenClaw Assistant

---

## 📋 技能描述

基于今天的实战经验，创建一个帮助用户快速创建 OpenClaw 定时任务的技能，避免踩坑。

---

## 🎯 核心功能

1. **引导式创建** - 通过问答方式收集任务信息
2. **最佳实践** - 自动应用今天的经验教训
3. **错误检查** - 检查常见配置错误
4. **模板生成** - 生成完整的任务配置

---

## 📝 今天的经验教训总结

### ❌ 踩过的坑

#### 坑 1: 用系统 crontab 而不是 OpenClaw cron
**错误做法**:
```bash
# ❌ 不要用系统 crontab
crontab -e
# 添加：0 8 * * * openclaw send "..."
```

**正确做法**:
```bash
# ✅ 使用 OpenClaw 内置 cron
openclaw cron add \
  --name "task-name" \
  --cron "0 8 * * *" \
  --message "任务描述" \
  --session "isolated"
```

**原因**:
- OpenClaw cron 有完整的管理功能
- 可以查看执行历史
- 支持错误重试
- 与 Gateway 集成

---

#### 坑 2: 没有配置记忆机制
**错误做法**:
- 直接创建任务，不记录偏好
- AI 每次都重新学习

**正确做法**:
```bash
# 创建记忆文件
vim ~/.openclaw/workspace/MEMORY.md
```

**记忆内容**:
```markdown
# 长期记忆

## 用户偏好
- 推送时间：每天早上 08:30
- 推送格式：简洁列表，带链接
- 关注领域：AI 技术、测试自动化

## 已读内容（避免重复）
- [已读] GPT-5-Codex 发布
- [已读] Qwen3-Next 开源
```

---

#### 坑 3: 没有配置心跳机制
**错误做法**:
- 创建任务后就不管了
- 任务挂了不知道

**正确做法**:
```bash
# 创建心跳配置
vim ~/.openclaw/workspace/HEARTBEAT.md
```

**心跳内容**:
```markdown
# HEARTBEAT.md

## 每日检查（每天 08:00）
- [ ] 检查定时任务是否正常
- [ ] 检查 API Key 是否有效
- [ ] 检查网络连接

## 异常处理
- 如果任务失败：立即通知
- 如果 API 失效：尝试重试 3 次
```

---

#### 坑 4: 没有处理依赖
**错误做法**:
```bash
# ❌ 脚本里直接用 jq
./tavily-search.sh | jq '.results'
# 结果：jq: command not found
```

**正确做法**:
```bash
# ✅ 用 Python 替代 jq
./tavily-search.sh | python3 -m json.tool

# 或者先检查依赖
which jq || brew install jq
```

---

#### 坑 5: 任务描述太模糊
**错误做法**:
```bash
openclaw cron add \
  --name "news" \
  --cron "0 8 * * *" \
  --message "推送新闻"
```

**正确做法**:
```bash
openclaw cron add \
  --name "ai-news-push-ykk" \
  --cron "0 7,9,11,13,15,17,19,21 * * *" \
  --message "使用 UltimateSearchSkill 搜索最新 AI 新闻，整理成简报推送到 YKK 家庭议事群" \
  --session "isolated" \
  --description "每天 07:00-21:00 每 2 小时推送新闻到 YKK 群"
```

---

#### 坑 6: 没有配置推送目标
**错误做法**:
```bash
# ❌ 没有指定推送目标
openclaw cron add \
  --name "news" \
  --message "推送新闻"
# 结果：推送失败，不知道推送到哪里
```

**正确做法**:
```bash
# ✅ 先获取推送目标 ID
# 飞书群聊 ID: oc_xxxxxxxxxxxx

# 然后配置
openclaw cron edit <task-id> --to "oc_xxxxxxxxxxxx"
```

---

#### 坑 7: 没有验证配置
**错误做法**:
```bash
# ❌ 创建完就不管了
openclaw cron add ...
# 结束
```

**正确做法**:
```bash
# ✅ 验证配置
openclaw cron list
openclaw cron status
openclaw cron runs --id <task-id>

# 测试运行
openclaw cron run <task-id>
```

---

### ✅ 最佳实践清单

#### 创建前准备
- [ ] 确认使用 OpenClaw cron，不是系统 crontab
- [ ] 准备好推送目标 ID（飞书 chat_id 或群 ID）
- [ ] 准备好 API Key（如 Tavily、Grok 等）
- [ ] 检查依赖（Python、jq 等）

#### 创建时配置
- [ ] 任务名称清晰（包含功能描述）
- [ ] Cron 表达式正确（用 cron 表达式生成器验证）
- [ ] 消息描述详细（包含具体操作步骤）
- [ ] 指定 session 为 isolated（后台执行）
- [ ] 添加 description（任务说明）

#### 创建后验证
- [ ] 运行 `openclaw cron list` 查看任务
- [ ] 运行 `openclaw cron status` 查看状态
- [ ] 手动运行一次测试：`openclaw cron run <task-id>`
- [ ] 检查推送是否成功

#### 配套配置
- [ ] 创建 MEMORY.md（记录偏好和历史）
- [ ] 创建 HEARTBEAT.md（配置心跳检查）
- [ ] 配置心跳任务：`openclaw cron add --name "heartbeat" ...`

---

## 🛠️ 技能使用流程

### Step 1: 运行技能
```bash
openclaw skill run cron-task-creator
```

### Step 2: 回答引导问题

技能会问以下问题：

**问题 1**: 任务名称是什么？
```
建议格式：<功能>-<目标>-<频率>
例如：ai-news-push-ykk-daily
```

**问题 2**: 任务执行频率？
```
选项：
1. 每小时
2. 每天固定时间
3. 每天多个时间
4. 每周
5. 自定义

推荐：用 cron 表达式生成器验证
工具：https://cron.qqe2.com/
```

**问题 3**: 任务具体做什么？
```
请详细描述：
1. 使用什么技能
2. 执行什么操作
3. 输出什么结果
4. 推送到哪里

示例：
"使用 UltimateSearchSkill 搜索最新 AI 新闻，
整理成包含 5-10 条的简报，
推送到 YKK 家庭议事群（oc_xxxxxxxxxxxx）"
```

**问题 4**: 推送目标是什么？
```
飞书：
- 个人：ou_xxxxxxxxxxxx
- 群聊：oc_xxxxxxxxxxxx

微信：
- 手机号（带国家码）：+8613800138000

Telegram:
- Chat ID: -100xxxxxxxxxx
```

**问题 5**: 是否需要心跳检查？
```
推荐：是

心跳检查内容：
- 任务是否正常执行
- API Key 是否有效
- 网络连接是否正常
- 磁盘空间是否充足
```

### Step 3: 自动生成配置

技能会生成以下内容：

**1. Cron 任务配置**:
```bash
openclaw cron add \
  --name "ai-news-push-ykk-daily" \
  --cron "0 8 * * *" \
  --message "使用 UltimateSearchSkill 搜索最新 AI 新闻，整理成简报推送到 YKK 家庭议事群" \
  --session "isolated" \
  --description "每天早上 8 点推送 AI 新闻"
```

**2. 记忆配置**:
```markdown
# MEMORY.md

## 任务历史
- 2026-03-05: 创建 ai-news-push-ykk-daily 任务

## 推送偏好
- 时间：每天 08:00
- 格式：简洁列表
- 目标：YKK 家庭议事群
```

**3. 心跳配置**:
```markdown
# HEARTBEAT.md

## 每日检查
- [ ] ai-news-push-ykk-daily 任务状态
- [ ] API Key 有效性
- [ ] 网络连接
```

**4. 验证命令**:
```bash
# 查看任务
openclaw cron list

# 查看状态
openclaw cron status

# 手动测试
openclaw cron run <task-id>

# 查看执行历史
openclaw cron runs --id <task-id>
```

### Step 4: 执行配置

技能会问：
```
是否立即执行上述配置？
1. 是，全部执行
2. 否，我手动执行
3. 只执行部分配置
```

### Step 5: 验证结果

执行后，技能会引导验证：
```
✅ 任务创建成功
✅ 记忆文件已更新
✅ 心跳配置已创建

请确认：
1. 运行 openclaw cron list 查看任务
2. 等待下次执行时间
3. 检查推送是否成功
```

---

## 📋 常用 Cron 表达式参考

| 频率 | Cron 表达式 | 说明 |
|------|-----------|------|
| 每分钟 | `* * * * *` | 每分钟执行 |
| 每小时 | `0 * * * *` | 每小时整点 |
| 每天早上 8 点 | `0 8 * * *` | 每天 8:00 |
| 每天早上 8 点和晚上 8 点 | `0 8,20 * * *` | 每天两次 |
| 每 2 小时 | `0 */2 * * *` | 0,2,4,6...点 |
| 每工作日 9 点 | `0 9 * * 1-5` | 周一到周五 |
| 每周日上午 10 点 | `0 10 * * 0` | 每周日 |
| 每月 1 号 | `0 0 1 * *` | 每月 1 号 |

---

## 🔧 故障排查

### 问题 1: 任务没有执行
**检查步骤**:
```bash
# 1. 查看任务状态
openclaw cron list

# 2. 查看 Gateway 状态
openclaw gateway status

# 3. 查看任务历史
openclaw cron runs --id <task-id>

# 4. 查看日志
openclaw cron runs --id <task-id> --json | tail -20
```

**常见原因**:
- Gateway 没有运行
- Cron 表达式错误
- Session 配置错误

---

### 问题 2: 推送失败
**检查步骤**:
```bash
# 1. 查看推送目标是否正确
openclaw cron edit <task-id> --to "oc_xxxxxxxxxxxx"

# 2. 测试推送
openclaw send --target "oc_xxxxxxxxxxxx" "测试消息"

# 3. 查看错误日志
openclaw cron runs --id <task-id>
```

**常见原因**:
- 推送目标 ID 错误
- 飞书 Bot 权限不足
- 网络问题

---

### 问题 3: API 调用失败
**检查步骤**:
```bash
# 1. 检查 API Key
echo $TAVILY_API_KEY

# 2. 测试 API
curl -X POST https://api.tavily.com/search \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# 3. 更新 API Key
export TAVILY_API_KEY="tvly-xxxxxxxxxxx"
```

**常见原因**:
- API Key 过期
- API Key 额度用完
- API 服务不可用

---

### 问题 4: 依赖缺失
**检查步骤**:
```bash
# 检查 Python
python3 --version

# 检查 jq
which jq

# 检查 curl
which curl
```

**安装依赖**:
```bash
# macOS
brew install python jq curl

# Ubuntu/Debian
apt-get install python3 jq curl
```

---

## 📚 相关文档

- [OpenClaw Cron 文档](https://docs.openclaw.ai/cli/cron)
- [Cron 表达式生成器](https://cron.qqe2.com/)
- [飞书 Bot 配置](https://open.feishu.cn/document/)
- [Tavily API 文档](https://docs.tavily.com/)

---

## 🎯 技能文件结构

```
~/.openclaw/workspace/skills/cron-task-creator/
├── SKILL.md          # 本文件
├── create-cron.sh    # 创建脚本
├── templates/        # 模板文件
│   ├── memory.md
│   ├── heartbeat.md
│   └── cron-config.sh
└── examples/         # 示例配置
    ├── news-push.sh
    ├── github-explorer.sh
    └── daily-report.sh
```

---

## 🚀 快速开始

**最简单的创建流程**:
```bash
# 1. 运行技能
openclaw skill run cron-task-creator

# 2. 回答问题
- 任务名称：my-task
- 执行频率：每天 8 点
- 任务描述：推送新闻
- 推送目标：oc_xxxxxxxxxxxx
- 心跳检查：是

# 3. 确认配置
# 4. 验证结果
```

**完成！** 🎉

---

*版本：1.0*  
*最后更新：2026-03-05*  
*基于今天的实战经验总结*
