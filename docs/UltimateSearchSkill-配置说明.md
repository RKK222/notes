# UltimateSearchSkill 配置说明

> 安装时间：2026-03-02  
> 状态：✅ 已安装，待配置 API Key

---

## 📦 安装位置

```
~/.openclaw/workspace/skills/UltimateSearchSkill/
~/.openclaw/workspace/skills/ultimate-search/ (软链接)
```

---

## 🎯 触发方式（重要！）

### ✅ 当前配置：**严格手动触发**

技能**仅在明确指令时触发**，必须包含技能名称。

**触发条件**（必须包含以下关键词）：
- ✅ "使用 ultimatesearch 技能"
- ✅ "用 ultimatesearch 搜索"
- ✅ "调用 ultimatesearch"
- ✅ "ultimatesearch: XXX"

**不会触发**（没有提到技能名）：
- ❌ "搜索 XXX"
- ❌ "检索一下 XXX"
- ❌ "查一下 XXX 的最新信息"
- ❌ 任何没有提到 "ultimatesearch" 的请求

**默认行为**：
- 所有问题 → 优先用内部知识回答
- 需要搜索时 → 先问"需要我使用 ultimatesearch 技能搜索吗？"
- 用户确认后 → 才调用技能

---

## ⚙️ 配置 API Key（使用前必须）

### 方式 1：简单配置（推荐）

编辑 `~/.openclaw/workspace/skills/UltimateSearchSkill/.env`：

```bash
# Grok SSO Token（至少 1 个）
# 获取方法：浏览器访问 https://grok.com → F12 → Cookies → sso
GROK_SSO_TOKENS=eyJhbGciOiJIUzI1NiJ9.xxx...

# Tavily API Key（免费 1000 次/月）
# 获取：https://www.tavily.com
TAVILY_API_KEYS=tvly-你的 key

# FireCrawl（可选，作为降级方案）
# 获取：https://www.firecrawl.dev
FIRECRAWL_API_KEY=fc-你的 key
```

### 方式 2：完整配置（Docker）

需要部署 Docker 服务（适合高频使用）：

```bash
cd ~/.openclaw/workspace/skills/UltimateSearchSkill
docker compose up -d
```

---

## 📝 使用示例

### 在飞书里对我说：

```
帮我搜索一下 2026 年最新的 AI 测试工具
```

```
检索小红书上的上海旅游攻略
```

```
查一下 TDD 和 BDD 的区别
```

### 我会：

1. 确认是否需要搜索
2. 调用 UltimateSearchSkill
3. 返回搜索结果
4. 整理成易读的格式

---

## 🔧 修改触发规则

如果你想**更频繁**或**更少**使用搜索：

### 方案 A：修改 AGENTS.md

编辑 `~/.openclaw/workspace/AGENTS.md` 的 Tools 部分：

```markdown
### 🔍 搜索工具

**触发规则**：
- 总是自动搜索：遇到事实性问题自动搜索
- 从不自动搜索：只在明确指令时搜索（当前配置）
- 询问后搜索：先问用户是否需要搜索（推荐）
```

### 方案 B：在 TOOLS.md 配置

创建 `~/.openclaw/workspace/TOOLS.md`：

```markdown
### 搜索偏好

- 默认：先询问是否需要搜索
- 例外：时间敏感信息（天气、新闻）可以直接搜索
- 禁止：不要搜索 XXX 类信息
```

---

## 💰 费用说明

### 免费额度

| 服务 | 免费额度 | 刷新周期 |
|------|---------|---------|
| Grok Basic | 80 次 | 每 20 小时 |
| Tavily Free | 1000 次 | 每月 |
| FireCrawl Free | 500 次 | 每月 |

### 监控用量

```bash
# 查看搜索次数
cat ~/.openclaw/workspace/skills/UltimateSearchSkill/logs/*.log | wc -l
```

---

## 🚀 快速测试

配置好 API Key 后，测试：

```bash
cd ~/.openclaw/workspace/skills/UltimateSearchSkill
source .env
bash scripts/tavily-search.sh --query "test" --max-results 1
```

---

## ❓ 常见问题

### Q: 每次都要说"搜索"吗？
A: 是的，这是当前配置。如果想改，看上面的"修改触发规则"。

### Q: 免费额度够用吗？
A: 个人日常使用完全够用（每天 20-30 次搜索）。

### Q: 可以自动搜索吗？
A: 可以，修改 AGENTS.md 配置为"总是自动搜索"。

### Q: 搜索失败怎么办？
A: 检查 API Key 是否过期，或切换其他搜索引擎。

---

## 📚 相关文档

- 完整文档：`~/.openclaw/workspace/skills/UltimateSearchSkill/README.md`
- 技能说明：`~/.openclaw/workspace/skills/UltimateSearchSkill/SKILL.md`
- 架构说明：`~/.openclaw/workspace/skills/UltimateSearchSkill/docs/architecture.md`

---

*最后更新：2026-03-02*
