# GitHub + 学术论坛深度探索技能

**技能名称**: `github-daily-explorer`  
**版本**: 1.0  
**创建时间**: 2026-03-05  
**作者**: OpenClaw Assistant

---

## 📋 技能描述

每天自动探索 GitHub 和学术论坛，寻找高质量、有趣的项目和论文，深度学习后推送给用户。

**执行时间**: 每天 11:00 和 19:00  
**推送方式**: 飞书  
**筛选标准**: 质量优先、新颖性、实用性

---

## 🎯 核心功能

1. **GitHub Trending 搜索** - 发现热门项目
2. **学术论文搜索** - arXiv 等学术论坛
3. **新兴项目挖掘** - 低星但高质量的项目
4. **深度分析报告** - 不只是列表，还有分析
5. **记忆系统** - 避免重复推送
6. **质量筛选** - 注重质量而非数量

---

## 🚀 快速开始

### Step 1: 安装技能
```bash
cd /Users/kaka/.openclaw/workspace/skills
# 技能已创建
```

### Step 2: 配置推送目标
```bash
# 编辑 explore.sh
PUSH_TARGET="oc_1df73fc9673b4412982efa8601317d97"
```

### Step 3: 创建定时任务
```bash
openclaw cron add \
  --name "github-daily-explorer" \
  --cron "0 11,19 * * *" \
  --message "深度探索 GitHub 和学术论坛，寻找高质量项目和论文，学习后推送报告" \
  --session "isolated" \
  --description "每天 11:00 和 19:00 推送 GitHub+ 学术探索报告"
```

### Step 4: 测试运行
```bash
cd /Users/kaka/.openclaw/workspace/skills/github-daily-explorer
./explore.sh
```

---

## 📊 推送内容

### 每次推送包含：

**1. Top 推荐项目（3 个）**
- 项目名称和链接
- Star 数
- 简介
- 推荐理由（技术新颖性/实用性/学习价值）
- 深度分析

**2. Top 推荐论文（3 篇）**
- 论文标题和链接
- 简介
- 研究价值（创新性/实用性/影响力）
- 核心贡献

**3. 新兴项目（2 个）**
- 低星但高质量
- 潜力评估
- 为什么值得关注

**4. 探索统计**
- 搜索数量
- 推荐数量
- 分类统计

**5. 深度学习建议**
- 今天最值得深入的项目
- 今天最值得阅读的论文

---

## 📁 文件结构

```
github-daily-explorer/
├── SKILL.md          # 本文件
├── explore.sh        # 主脚本
├── memory/           # 记忆文件
│   └── github-daily.md
└── reports/          # 历史报告
    └── YYYY-MM-DD.md
```

---

## 🔧 配置选项

### 推送频率
```bash
# 每天两次（11:00 和 19:00）
--cron "0 11,19 * * *"

# 每天一次（早上 9:00）
--cron "0 9 * * *"

# 工作日每天两次
--cron "0 11,19 * * 1-5"
```

### 搜索范围
```bash
# GitHub trending
./tavily-search.sh --query "GitHub trending projects AI"

# 学术论文
./tavily-search.sh --query "arXiv AI agent paper"

# 新兴项目
./tavily-search.sh --query "GitHub new project under 100 stars"
```

### 推送目标
```bash
# 飞书群
PUSH_TARGET="oc_xxxxxxxxxxxx"

# 飞书个人
PUSH_TARGET="ou_xxxxxxxxxxxx"
```

---

## 📝 记忆机制

### 记忆文件位置
```
~/.openclaw/workspace/memory/github-daily.md
```

### 记忆内容
```markdown
## 2026-03-05 11:00 探索记录
- 搜索 GitHub trending: 10 个项目
- 搜索学术论文：10 篇论文
- 推荐项目：3 个
- 推荐论文：3 篇
- 新兴项目：2 个
- 已推送项目：
  - [ ] Project A
  - [ ] Paper B
```

### 避免重复
每次推送前检查记忆文件，避免重复推送相同内容。

---

## 💡 质量标准

### 项目筛选标准
- ⭐ **技术新颖性**: 是否有创新？
- ⭐ **实用性**: 是否能解决实际问题？
- ⭐ **学习价值**: 是否能学到东西？
- ⭐ **代码质量**: 代码是否规范？
- ⭐ **文档完善**: 文档是否清晰？

### 论文筛选标准
- ⭐ **创新性**: 是否有新贡献？
- ⭐ **实用性**: 是否有应用价值？
- ⭐ **影响力**: 是否可能影响领域？
- ⭐ **可复现性**: 是否有代码/数据？
- ⭐ **写作质量**: 是否清晰易懂？

---

## 🔍 搜索源

### GitHub
- Trending 页面
- Topics 页面
- Explore 页面

### 学术论坛
- arXiv (https://arxiv.org/)
- Papers With Code (https://paperswithcode.com/)
- Google Scholar
- Semantic Scholar

### 社区
- Hacker News
- Reddit r/MachineLearning
- Twitter AI 社区

---

## 📈 推送示例

```
🦞 GitHub + 学术论坛深度探索报告

探索时间：03-05 11:00

📌 今日推荐:

### 项目推荐
1. Project A - AI 自动化新框架
2. Project B - 低代码 Agent 平台
3. Project C - 新型 RAG 引擎

### 论文推荐
1. Paper A - 多 Agent 协作新突破
2. Paper B - 自主学习的理论分析
3. Paper C - 高效推理新方法

📄 完整报告已保存到：github-daily-report.md
```

---

## ⚠️ 注意事项

1. **API 限制**: Tavily 有免费额度限制（1000 次/月）
2. **推送频率**: 每天 2 次，避免打扰
3. **内容质量**: 宁缺毋滥，确保推荐质量
4. **记忆更新**: 每次推送后更新记忆
5. **错误处理**: 失败时记录日志

---

## 🐛 故障排查

### 问题 1: 推送失败
```bash
# 检查 Bot Token
# 编辑 explore.sh，确认 PUSH_TARGET 正确
```

### 问题 2: 搜索结果为空
```bash
# 检查网络连接
curl https://api.tavily.com

# 检查 API Key
echo $TAVILY_API_KEY
```

### 问题 3: 报告生成失败
```bash
# 检查 Python3
python3 --version

# 检查权限
chmod +x explore.sh
```

---

## 📚 相关文档

- [OpenClaw Cron 文档](https://docs.openclaw.ai/cli/cron)
- [Tavily API 文档](https://docs.tavily.com/)
- [GitHub Trending](https://github.com/trending)
- [arXiv](https://arxiv.org/)

---

*版本：1.0*  
*最后更新：2026-03-05*  
*基于用户需求创建*
