# Superpowers 仓库学习文档

> 学习时间：2026-03-02  
> 仓库：https://github.com/obra/superpowers  
> 作者：Jesse Vincent (@obra)

---

## 📦 仓库概览

### 核心数据
- **Stars**: 67.4k
- **Forks**: 5.2k
- **Commits**: 286
- **最后更新**: 2026 年 2 月 22 日
- **License**: MIT
- **主要语言**: Shell 76.4%, JavaScript 12.4%, Python 5.7%, TypeScript 4.3%

### 这是什么？
**Superpowers** 是一个完整的**智能体编码工作流框架**，基于可组合的 "skills" 系统构建。它不是直接写代码，而是提供一套完整的方法论和工具集，让 AI 编码智能体能够：
- 先理解需求再动手
- 系统化设计和规划
- 强制 TDD 工作流
- 多智能体协作执行

---

## 🎯 核心工作原理

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 1. 需求澄清  │ →  │ 2. 设计确认  │ →  │ 3. 计划制定  │ →  │ 4. 子智能体  │ →  │ 5. 代码审查  │
│             │    │             │    │             │    │    执行     │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 关键流程

1. **不直接写代码** - 智能体先问用户真正想做什么
2. **分块展示设计** - 短到可以真正阅读消化
3. **详细实现计划** - 清晰到初级工程师能跟随
4. **子智能体驱动开发** - 每个任务由独立子智能体完成
5. **强制 TDD** - RED-GREEN-REFACTOR 循环

---

## 📚 Skills 库详解

### 测试相关

| Skill | 说明 |
|-------|------|
| `test-driven-development` | RED-GREEN-REFACTOR 完整循环，包含测试反模式参考 |

### 调试相关

| Skill | 说明 |
|-------|------|
| `systematic-debugging` | 4 阶段根因分析流程 (根因追踪、纵深防御、条件等待) |
| `verification-before-completion` | 确保问题真正被修复 |

### 协作相关

| Skill | 说明 |
|-------|------|
| `brainstorming` | 苏格拉底式设计优化，通过提问 refine 需求 |
| `writing-plans` | 详细实现计划，每个任务 2-5 分钟，包含完整代码和验证步骤 |
| `executing-plans` | 带人工检查点的批量执行 |
| `dispatching-parallel-agents` | 并发子智能体工作流 |
| `requesting-code-review` | 预审查清单 |
| `receiving-code-review` | 如何响应反馈 |
| `using-git-worktrees` | 并行开发分支管理 |
| `finishing-a-development-branch` | 合并/PR/保留/丢弃决策工作流 |
| `subagent-driven-development` | 两阶段审查 (规范符合性 → 代码质量) |

### Meta

| Skill | 说明 |
|-------|------|
| `writing-skills` | 创建新技能的最佳实践指南 |
| `using-superpowers` | 技能系统入门 |

---

## 🛠️ 支持平台

### Claude Code
```bash
# 注册市场
/plugin marketplace add obra/superpowers-marketplace

# 安装插件
/plugin install superpowers@superpowers-marketplace
```

### Cursor
```bash
/plugin-add superpowers
```

### Codex
```bash
# 告诉 Codex 获取并执行安装指令
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
```

### OpenCode
```bash
# 告诉 OpenCode 获取并执行安装指令
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

### 验证安装
启动新会话并请求触发技能（如 "help me plan this feature"），智能体应自动调用相关 superpowers skill。

---

## 💡 核心理念

1. **Test-Driven Development** - 总是先写测试
2. **Systematic over ad-hoc** - 流程胜过猜测
3. **Complexity reduction** - 简洁是首要目标
4. **Evidence over claims** - 验证后再宣布成功

---

## 📁 仓库结构

```
superpowers/
├── .claude-plugin/     # Claude 插件配置
├── .cursor-plugin/     # Cursor 插件配置
├── .codex/            # Codex 安装说明
├── .opencode/         # OpenCode 安装说明
├── .github/           # GitHub 配置
├── agents/            # 智能体配置
├── commands/          # 斜杠命令
├── docs/              # 详细文档
├── hooks/             # Git hooks
├── lib/               # 核心库 (ESM 模块)
├── skills/            # 技能库
├── tests/             # 测试
├── README.md          # 主文档
├── RELEASE-NOTES.md   # 发布说明
└── LICENSE            # MIT 许可证
```

---

## 🔄 基本工作流

1. **brainstorming** - 写代码前激活，通过提问 refine 需求，展示设计章节供验证
2. **using-git-worktrees** - 设计批准后激活，创建隔离工作区，运行项目设置
3. **writing-plans** - 将工作分解为小任务 (2-5 分钟每个)，包含完整代码和验证
4. **subagent-driven-development** - 每个任务由新子智能体执行，两阶段审查
5. **test-driven-development** - 强制执行 RED-GREEN-REFACTOR
6. **requesting-code-review** - 任务间审查，按严重性报告问题
7. **finishing-a-development-branch** - 验证测试，提供合并/PR/保留/丢弃选项

**关键**: 智能体在执行任何任务前检查相关技能。这是强制工作流，不是建议。

---

## 📖 相关资源

- **博客文章**: [Superpowers for Claude Code](https://blog.fsck.com/2025/10/09/superpowers/)
- **插件市场**: https://github.com/obra/superpowers-marketplace
- **问题追踪**: https://github.com/obra/superpowers/issues

---

## 🤝 贡献指南

技能直接存放在此仓库。贡献步骤：
1. Fork 仓库
2. 创建技能分支
3. 遵循 `skills/writing-skills/SKILL.md` 创建和测试新技能
4. 提交 PR

---

## 📌 学习心得

### 核心价值
1. **方法论优先** - 不是简单的工具集，而是完整的开发哲学
2. **强制纪律** - 通过技能系统强制执行 TDD 和代码审查
3. **可扩展** - 技能库可以持续扩展
4. **平台无关** - 支持多个 AI 编码平台

### 适用场景
- 需要系统化 AI 辅助开发的团队
- 想要强制 TDD 工作流的项目
- 多智能体协作的大型项目
- 需要代码质量保障的场景

### 局限性
- 需要学习曲线
- 对小型快速原型可能过度
- 依赖 AI 编码平台支持

---

## 📄 核心 Skill 详解：Test-Driven-Development

### 核心原则
> **Write the test first. Watch it fail. Write minimal code to pass.**

### 铁律
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
- 先写代码后写测试？删除它，重新开始
- 不要保留作"参考"
- 不要"适配"它

### RED-GREEN-REFACTOR 循环

```
RED → 写失败测试 → 验证失败原因 → GREEN → 写最简代码 → 验证通过 → REFACTOR → 清理代码
```

**RED 阶段要求：**
- 一个行为一个测试
- 清晰的测试名
- 真实代码（避免 mock）

**验证 RED（强制）：**
- 测试失败（不是报错）
- 失败信息符合预期
- 因为功能缺失而失败（不是拼写错误）

**GREEN 阶段：**
- 只写能通过测试的最简代码
- 不要添加额外功能
- 不要"优化"

**验证 GREEN（强制）：**
- 测试通过
- 其他测试仍通过
- 输出干净（无错误警告）

**REFACTOR 阶段：**
- 移除重复
- 改进命名
- 提取辅助函数
- 保持测试绿色

### 常见借口 vs 现实

| 借口 | 现实 |
|------|------|
| "太简单不用测试" | 简单代码也会坏，测试只要 30 秒 |
| "我稍后写测试" | 测试立即通过证明不了什么 |
| "已经手动测试了" | 手动=临时，自动=系统化 |
| "删除 X 小时工作太浪费" | 沉没成本谬误，保留不可信代码才是技术债 |
| "TDD 太教条，要务实" | TDD 就是务实，调试生产环境更慢 |

### 危险信号（停止并重来）
- 代码在测试之前
- 测试在实现之后
- 测试立即通过
- 无法解释为什么测试失败
- "我已经手动测试了"
- "这只是例外"

**所有这些意味着：删除代码，用 TDD 重新开始**

### 验证清单
- [ ] 每个新函数/方法都有测试
- [ ] 看着每个测试失败后再实现
- [ ] 每个测试因预期原因失败
- [ ] 写最简代码通过每个测试
- [ ] 所有测试通过
- [ ] 输出干净
- [ ] 测试使用真实代码
- [ ] 边界情况和错误已覆盖

---

*文档由 LitteleAurora 整理生成*  
*最后更新：2026-03-02 17:10 CST*  
*已下载完整仓库代码*
