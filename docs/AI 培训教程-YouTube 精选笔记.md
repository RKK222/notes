# AI 培训教程 - YouTube 精选笔记

**整理时间**: 2026-03-04  
**来源**: YouTube 热门 AI 教程视频  
**整理者**: LitteleAurora

---

## 📚 目录

1. [提示词工程核心框架](#1-提示词工程核心框架)
2. [Skills 使用技巧](#2-skills 使用技巧)
3. [多 Agent 协作实战](#3-多 agent 协作实战)
4. [推荐学习路径](#4-推荐学习路径)
5. [视频资源链接](#5-视频资源链接)

---

## 1. 提示词工程核心框架

### 1.1 完整提示词结构

一个高质量的提示词应该包含以下四个部分：

```markdown
# Identity（身份）
- 你是什么角色（AI 助手/专家/顾问）
- 沟通风格（正式/轻松/专业/幽默）
- 高层目标（帮助用户解决问题/提供建议/执行任务）

# Instructions（指令）
- 遵循什么规则（格式要求/长度限制/语言要求）
- 能做什么/不能做什么（边界设定）
- 如何调用工具/Skills（如果有）

# Examples（示例）
- 输入输出示例（展示期望格式）
- Few-shot learning（少样本学习）
- 正确 vs 错误对比

# Context（上下文）
- 专有数据（用户提供的背景信息）
- 参考材料（相关文档/链接）
- RAG 检索内容（检索增强生成）
```

### 1.2 消息角色优先级

```
developer > user > assistant
```

**比喻理解**：
- `developer` = 函数定义（系统规则和业务逻辑）
- `user` = 函数参数（用户输入和配置）
- `assistant` = 函数返回值（AI 回复）

**实战示例**：
```python
# 系统指令（developer 角色）
system_prompt = """
你是一个专业的 Python 代码助手。
- 只回答 Python 相关问题
- 代码必须包含注释
- 优先使用 Python 3.10+ 特性
"""

# 用户输入（user 角色）
user_input = "如何读取 JSON 文件？"

# AI 回复（assistant 角色）
# import json
# with open('data.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
```

### 1.3 消息格式化技巧

**使用 Markdown 和 XML 标签**：

```markdown
# Identity
你是客服助手，负责回答产品相关问题。

# Instructions
- 只回答产品相关问题
- 回答要简洁，不超过 200 字
- 如果不知道，就说"我需要查询一下"

# Examples
<user_query>这个产品多少钱？</user_query>
<assistant_response>产品价格是 ¥299，目前有 8 折优惠。</assistant_response>

# Context
<product_info>
产品名称：智能手表 X1
原价：¥399
现价：¥299
库存：100 件
</product_info>
```

### 1.4 Few-shot Learning（少样本学习）

**原理**：通过提供少量示例，让 AI 学会新模式

**示例 - 情感分类**：
```
输入："这耳机太棒了，音质超好！" → 输出：Positive
输入："电池还行，但耳垫有点夹耳朵。" → 输出：Neutral
输入："客服态度太差，再也不买了！" → 输出：Negative

现在请分类："物流很快，包装也很好，满意！"
```

**预期输出**：Positive

---

## 2. Skills 使用技巧

### 2.1 Skills 是什么？

**定义**：Skills 是 AI 的"插件系统"，让 AI 能够调用外部工具和服务。

**类比**：就像手机 App 扩展功能一样，Skills 让 AI 能做更多事情。

### 2.2 常见 Skills 类型

| 类型 | 功能 | 示例 |
|------|------|------|
| 🔍 **搜索类** | 网络搜索、信息检索 | Web Search, Google Search |
| 💻 **代码类** | 代码执行、调试 | Code Interpreter, Python Runner |
| 📁 **文件类** | 文件读写、搜索 | File Search, Document Reader |
| 🔗 **连接类** | API 调用、服务集成 | MCP Connector, API Client |
| 🎨 **创作类** | 图片生成、视频制作 | Image Generation, Video Creator |
| 📊 **分析类** | 数据分析、图表生成 | Data Analyzer, Chart Maker |

### 2.3 Skills 实战流程

```
步骤 1: 安装 Skill
    ↓
步骤 2: 配置参数（API Key、认证信息等）
    ↓
步骤 3: 在对话中调用
    ↓
步骤 4: 查看结果并迭代
```

### 2.4 实战示例

**示例 1：使用 Web Search Skill**
```
用户：帮我查一下 2026 年 AI 发展趋势

AI: [调用 Web Search Skill]
    → 搜索"2026 AI trends"
    → 获取搜索结果
    → 整理汇总

AI: 2026 年 AI 发展主要有以下趋势：
1. AI Agent 普及化
2. 多模态模型成熟
3. 边缘 AI 部署增加
...
```

**示例 2：使用 Code Interpreter Skill**
```
用户：帮我计算 1 到 100 的素数之和

AI: [调用 Code Interpreter Skill]
    → 执行 Python 代码
    → def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    → print(sum(i for i in range(1, 101) if is_prime(i)))
    → 输出：1060

AI: 1 到 100 的素数之和是 1060
```

### 2.5 Skills 安装命令

```bash
# 通过 clawhub 安装
clawhub install <skill-name>

# 通过 npx 安装
npx skills install <skill-name>

# 查看已安装 Skills
clawhub list
```

---

## 3. 多 Agent 协作实战

### 3.1 为什么需要多 Agent？

**单一 AI 的局限性**：
- 能力有限，难以处理复杂任务
- 上下文窗口限制
- 专业领域知识不足

**多 Agent 的优势**：
- 分工协作，各司其职
- 可以处理更复杂的任务
- 提高准确性和效率

### 3.2 协作模式

#### 模式 1：流水线式
```
用户输入 → Agent A(分析) → Agent B(执行) → Agent C(审核) → 输出
```

**适用场景**：需要多步骤处理的任务

**示例**：
```
用户：帮我写一份市场分析报告

Agent A (研究员): 收集市场数据
    ↓
Agent B (分析师): 分析数据，提取洞察
    ↓
Agent C (作家): 撰写报告
    ↓
输出：完整的市场分析报告
```

#### 模式 2：主从式
```
        主 Agent (协调者)
       /    |    \
      ↓     ↓     ↓
  Agent A  Agent B  Agent C
  (搜索)   (分析)   (写作)
```

**适用场景**：需要并行处理的任务

#### 模式 3：讨论式
```
Agent A ─┐
         ├→ 讨论 → 共识 → 输出
Agent B ─┘
```

**适用场景**：需要多角度分析的任务

### 3.3 OpenClaw 多 Agent 配置

**配置文件示例** (`agents.yaml`)：
```yaml
agents:
  - name: researcher
    role: 信息收集
    skills: [web-search, document-reader]
    
  - name: analyst
    role: 数据分析
    skills: [data-analyzer, chart-maker]
    
  - name: writer
    role: 内容创作
    skills: [content-writer, translator]

workflow:
  - step: 1
    agent: researcher
    task: 收集相关信息
  - step: 2
    agent: analyst
    task: 分析收集的信息
  - step: 3
    agent: writer
    task: 撰写最终报告
```

### 3.4 实战案例

**案例：自动化客服系统**

```
用户问题 → 分类 Agent → 路由到对应专业 Agent
                              ↓
                    ┌───────┬───────┬───────┐
                    ↓       ↓       ↓       ↓
                技术支援  账单查询  产品咨询  投诉处理
                    ↓       ↓       ↓       ↓
                    └───────┴───────┴───────┘
                              ↓
                        回复用户
```

---

## 4. 推荐学习路径

### 第 1 天：基础入门

**学习目标**：
- 理解 AI 基础概念
- 安装并配置 OpenClaw
- 掌握基础对话技巧

**学习内容**：
1. 观看视频：【保姆级】OpenClaw 全网最细教学 (53 分钟)
2. 安装 OpenClaw
3. 练习基础对话

**实践任务**：
```
- 完成 OpenClaw 安装
- 尝试 10 次以上对话
- 记录遇到的问题和解决方案
```

### 第 2 天：Skills 实战

**学习目标**：
- 理解 Skills 概念
- 安装并配置 2-3 个 Skills
- 掌握 Skills 调用方法

**学习内容**：
1. 观看视频：Agent Skill 从使用到原理 (17 分钟)
2. 安装 Skills（推荐：web-search, code-interpreter）
3. 实战练习

**实践任务**：
```
- 安装 2 个 Skills
- 每个 Skills 至少使用 5 次
- 记录使用心得
```

### 第 3 天：高级应用

**学习目标**：
- 理解多 Agent 协作
- 搭建简单的工作流
- 掌握提示词工程技巧

**学习内容**：
1. 观看视频：Claude Cowork 自动化团队 (16 分钟)
2. 学习提示词工程框架
3. 搭建多 Agent 工作流

**实践任务**：
```
- 设计一个多 Agent 工作流
- 实现一个自动化任务
- 撰写学习总结
```

### 第 4-7 天：项目实战

**学习目标**：
- 综合运用所学知识
- 完成一个完整项目
- 形成自己的最佳实践

**项目建议**：
```
选项 1: 自动化新闻汇总系统
选项 2: 智能客服助手
选项 3: 数据分析报告生成器
选项 4: 个人知识管理系统
```

---

## 5. 视频资源链接

### 5.1 必看电影

| 视频 | 链接 | 时长 | 难度 |
|------|------|------|------|
| 【保姆级】OpenClaw 全网最细教学 | https://www.youtube.com/watch?v=2ZZCyHzo9as | 53:25 | ⭐⭐ |
| Agent Skill 从使用到原理 | https://www.youtube.com/watch?v=yDc0_8emz7M | 17:42 | ⭐⭐⭐ |
| Claude Cowork 自动化团队 | https://www.youtube.com/watch?v=UkcMNFxeVKk | 16:10 | ⭐⭐⭐ |

### 5.2 进阶学习

| 视频 | 链接 | 时长 | 难度 |
|------|------|------|------|
| OpenClaw 海量全玩法攻略 | https://www.youtube.com/watch?v=657wlbtrzG8 | 11:41 | ⭐⭐⭐⭐ |
| 从 Claude 小卖部实验破产看 AI 落地 | https://www.youtube.com/watch?v=vd1XoGasyXw | 28:12 | ⭐⭐⭐⭐ |
| 2026 年的机会在哪儿 | https://www.youtube.com/watch?v=LQjOUGdJ4ec | 14:58 | ⭐⭐⭐ |

### 5.3 最新动态

| 视频 | 链接 | 时长 | 说明 |
|------|------|------|------|
| OpenAI 发布 GPT-5.3 Instant | https://www.youtube.com/watch?v=v6xc7243Mu0 | 4:52 | 最新模型动态 |
| OpenClaw 爆火实测 | https://www.youtube.com/watch?v=Z2UUMEvFtx8 | 8:35 | Token 消耗分析 |

---

## 📝 附录：常用命令速查

### OpenClaw 基础命令
```bash
# 启动
openclaw gateway start

# 停止
openclaw gateway stop

# 重启
openclaw gateway restart

# 查看状态
openclaw gateway status
```

### Skills 管理命令
```bash
# 安装 Skill
clawhub install <skill-name>

# 卸载 Skill
clawhub uninstall <skill-name>

# 列出已安装
clawhub list

# 更新 Skill
clawhub update <skill-name>
```

### 配置命令
```bash
# 配置 API Key
openclaw configure --section api

# 配置模型
openclaw configure --section model

# 查看配置
openclaw config --show
```

---

## 🎯 学习检查清单

### 基础篇
- [ ] 理解 AI 基础概念
- [ ] 完成 OpenClaw 安装
- [ ] 能够进行基础对话
- [ ] 理解提示词结构

### 进阶篇
- [ ] 理解 Skills 概念
- [ ] 安装并使用 2 个以上 Skills
- [ ] 掌握提示词工程技巧
- [ ] 能够编写复杂提示词

### 高级篇
- [ ] 理解多 Agent 协作
- [ ] 搭建一个工作流
- [ ] 完成一个完整项目
- [ ] 形成自己的最佳实践

---

**最后更新**: 2026-03-04  
**维护者**: LitteleAurora  
**反馈**: 如有问题或建议，请联系小皇帝
