# 测试数据生成器 - 方案 B：场景模板驱动

> 设计时间：2026-03-03 00:30  
> 核心理念：选择业务场景，一键生成测试数据

---

## 🎯 方案概述

**用户输入**：业务场景（电商/支付/社交等）+ 数据量  
**自动处理**：加载场景模板 → 生成关联数据 → 导出  
**输出**：完整的业务场景测试数据

**适用场景**：
- ✅ 不知道有哪些表
- ✅ 没有接口文档
- ✅ 快速搭建测试环境
- ✅ 标准化测试数据

---

## 📋 使用流程

### 方式 1：命令行快速生成

```bash
# 电商场景 - 生成订单测试数据
testdata-gen --scenario ecommerce --type order --count 10

# 电商场景 - 生成完整流程数据
testdata-gen --scenario ecommerce --workflow full --count 10

# 支付场景 - 生成交易数据
testdata-gen --scenario payment --type transaction --count 100

# 社交场景 - 生成用户动态
testdata-gen --scenario social --type post --count 200
```

### 方式 2：交互式配置

```bash
# 启动交互式模式
testdata-gen --interactive

# 按向导选择：
# 1. 选择场景：电商/支付/社交/自定义
# 2. 选择数据类型：订单/用户/商品等
# 3. 输入生成数量
# 4. 选择导出格式
# 5. 开始生成
```

### 方式 3：配置文件

```yaml
# config.yaml
scenario: ecommerce
type: order
count: 10
relations:
  user_ratio: 5      # 1 个订单对应 5 个用户
  product_ratio: 2   # 1 个订单对应 2 个商品
output:
  format: json
  directory: ./test-data/
```

```bash
testdata-gen --config config.yaml
```

---

## 📦 内置场景模板

### 场景 1：电商（Ecommerce）

```yaml
# ecommerce.yaml
name: 电商场景
description: 在线购物、订单管理

tables:
  users:
    fields:
      - id: {type: int, primary_key: true}
      - username: {type: string, faker: user_name}
      - email: {type: string, faker: email}
      - phone: {type: string, faker: phone_number}
      - created_at: {type: datetime, faker: date_time}
    count: 50

  products:
    fields:
      - id: {type: int, primary_key: true}
      - name: {type: string, faker: catch_phrase}
      - price: {type: decimal, min: 9.9, max: 999.9}
      - stock: {type: int, min: 0, max: 1000}
      - category: {type: string, choices: [电子，服装，食品，家居]}
    count: 20

  orders:
    fields:
      - id: {type: int, primary_key: true}
      - user_id: {type: int, foreign_key: users.id}
      - total_amount: {type: decimal}
      - status: {type: string, choices: [pending, paid, shipped, completed]}
      - created_at: {type: datetime}
    count: 10
    relations:
      - table: order_items
        count: "2-5"  # 每个订单 2-5 个商品

  order_items:
    fields:
      - id: {type: int, primary_key: true}
      - order_id: {type: int, foreign_key: orders.id}
      - product_id: {type: int, foreign_key: products.id}
      - quantity: {type: int, min: 1, max: 10}
      - price: {type: decimal}
```

---

### 场景 2：支付（Payment）

```yaml
# payment.yaml
name: 支付场景
description: 交易、转账、结算

tables:
  accounts:
    fields:
      - id: {type: int, primary_key: true}
      - account_no: {type: string, faker: iban}
      - balance: {type: decimal, min: 0, max: 100000}
      - currency: {type: string, choices: [CNY, USD, EUR]}
    count: 100

  transactions:
    fields:
      - id: {type: int, primary_key: true}
      - from_account: {type: int, foreign_key: accounts.id}
      - to_account: {type: int, foreign_key: accounts.id}
      - amount: {type: decimal, min: 0.01, max: 10000}
      - type: {type: string, choices: [transfer, payment, refund]}
      - status: {type: string, choices: [pending, success, failed]}
    count: 500
```

---

### 场景 3：社交（Social）

```yaml
# social.yaml
name: 社交场景
description: 用户动态、评论、点赞

tables:
  users:
    fields:
      - id: {type: int, primary_key: true}
      - nickname: {type: string, faker: name}
      - avatar: {type: string, faker: image_url}
      - bio: {type: string, faker: sentence}
    count: 100

  posts:
    fields:
      - id: {type: int, primary_key: true}
      - user_id: {type: int, foreign_key: users.id}
      - content: {type: text, faker: paragraph}
      - images: {type: json, faker: image_urls}
      - like_count: {type: int, min: 0, max: 1000}
    count: 200

  comments:
    fields:
      - id: {type: int, primary_key: true}
      - post_id: {type: int, foreign_key: posts.id}
      - user_id: {type: int, foreign_key: users.id}
      - content: {type: text, faker: sentence}
    count: 1000
```

---

### 场景 4：内容管理（CMS）

```yaml
# cms.yaml
name: 内容管理场景
description: 文章、分类、标签

tables:
  categories:
    fields:
      - id: {type: int, primary_key: true}
      - name: {type: string}
      - parent_id: {type: int, foreign_key: categories.id}
    count: 10

  articles:
    fields:
      - id: {type: int, primary_key: true}
      - title: {type: string, faker: sentence}
      - content: {type: text, faker: paragraphs}
      - author_id: {type: int}
      - category_id: {type: int, foreign_key: categories.id}
      - view_count: {type: int, min: 0, max: 10000}
    count: 50

  tags:
    fields:
      - id: {type: int, primary_key: true}
      - name: {type: string}
    count: 20

  article_tags:
    fields:
      - article_id: {type: int, foreign_key: articles.id}
      - tag_id: {type: int, foreign_key: tags.id}
    count: 100
```

---

## 🖥️ 页面设计

### 页面 1：场景选择

```
┌─────────────────────────────────────────────┐
│  选择业务场景                         [×]   │
├─────────────────────────────────────────────┤
│                                             │
│  热门场景：                                 │
│  ┌─────────────┐  ┌─────────────┐          │
│  │ 🛒 电商     │  │ 💰 支付     │          │
│  │ 订单/用户/商品│  │ 交易/转账   │          │
│  │ [选择]     │  │ [选择]     │          │
│  └─────────────┘  └─────────────┘          │
│                                             │
│  ┌─────────────┐  ┌─────────────┐          │
│  │ 💬 社交     │  │ 📝 内容管理 │          │
│  │ 动态/评论/点赞│  │ 文章/分类/标签│         │
│  │ [选择]     │  │ [选择]     │          │
│  └─────────────┘  └─────────────┘          │
│                                             │
│  更多场景：                                 │
│  [教育] [医疗] [物流] [酒店] [自定义...]    │
│                                             │
│  [取消]                                     │
│                                             │
└─────────────────────────────────────────────┘
```

### 页面 2：数据类型选择

```
┌─────────────────────────────────────────────┐
│  电商场景 - 选择数据类型              [×]   │
├─────────────────────────────────────────────┤
│                                             │
│  请选择要生成的数据类型：                   │
│                                             │
│  ☑ 用户数据 (50 条)                         │
│     包含：用户名、邮箱、手机号、地址        │
│                                             │
│  ☑ 商品数据 (20 条)                         │
│     包含：商品名称、价格、库存、分类        │
│                                             │
│  ☑ 订单数据 (10 条)                         │
│     包含：订单号、金额、状态、时间          │
│                                             │
│  ☑ 订单项数据 (自动计算)                    │
│     每个订单 2-5 个商品                       │
│                                             │
│  数据量配置：                               │
│  用户：  [50   ] 条                         │
│  商品：  [20   ] 条                         │
│  订单：  [10   ] 条                         │
│                                             │
│  [上一步]            [下一步：生成配置]     │
│                                             │
└─────────────────────────────────────────────┘
```

### 页面 3：生成配置（同方案 A）

### 页面 4：生成结果（同方案 A）

---

## 🔧 核心功能设计

### 功能 1：场景模板引擎

```python
class ScenarioTemplate:
    """场景模板管理"""
    
    def load_scenario(self, name):
        """加载场景模板"""
        # 1. 从内置模板加载
        # 2. 或从自定义目录加载
        # 3. 验证模板格式
        
    def get_tables(self, scenario):
        """获取场景包含的表"""
        # 返回表结构和生成规则
        
    def calculate_counts(self, scenario, base_count):
        """计算各表生成数量"""
        # 根据比例自动计算
        # 如：订单 10 条 → 用户 50 条 → 商品 20 条
```

### 功能 2：数据生成器（同方案 A）

### 功能 3：自定义模板

```python
class CustomTemplate:
    """自定义场景模板"""
    
    def create_from_existing(self, db_connection):
        """从现有数据库创建模板"""
        # 1. 分析数据库表结构
        # 2. 推断表关系
        # 3. 生成模板 YAML
        
    def export_template(self, template, output_path):
        """导出模板"""
        
    def import_template(self, template_path):
        """导入模板"""
```

---

## 📊 数据流设计

```
┌──────────────┐
│ 用户选择场景 │
│ 电商/支付/社交│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 加载场景模板 │
│ - 表定义     │
│ - 字段规则   │
│ - 关联关系   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 计算生成数量 │
│ - 基础数量   │
│ - 比例计算   │
│ - 依赖排序   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 数据生成器   │
│ - 模板匹配   │
│ - 关联生成   │
│ - 一致性检查 │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 数据导出器   │
│ - JSON/CSV   │
│ - SQL        │
│ - ZIP        │
└──────────────┘
```

---

## ✅ 自检清单

### 功能完备性

- [x] 内置常用场景模板
- [x] 支持自定义模板
- [x] 自动计算关联数据量
- [x] 处理表依赖关系
- [x] 交互式配置向导
- [x] 命令行快速生成
- [x] 配置文件方式

### 用户体验

- [x] 场景可视化选择
- [x] 智能默认值
- [x] 数据量自动计算
- [x] 模板预览功能
- [x] 一键生成

### 技术可行性

- [x] YAML 模板易解析
- [x] Faker 数据生成成熟
- [x] 依赖排序有算法
- [x] 无不可实现功能

### 潜在问题

- [ ] 场景覆盖不全 → 支持自定义模板
- [ ] 特殊业务逻辑 → 提供扩展点
- [ ] 模板版本管理 → 添加版本号

---

## 🎯 与方案 A 的对比

| 维度 | 方案 A（接口驱动） | 方案 B（场景驱动） |
|------|------------------|------------------|
| 上手难度 | 中（需要接口文档） | 低（选择场景即可） |
| 灵活性 | 高（自定义接口） | 中（受模板限制） |
| 准确度 | 高（基于实际接口） | 中（通用模板） |
| 适用场景 | 有接口文档的项目 | 快速搭建/标准化测试 |
| 学习成本 | 中 | 低 |

---

## 🎯 下一步

**方案 B 设计完成**，等待：
1. 方案 C（AI 智能驱动）设计
2. 三套方案对比和自检

---

*方案设计完成时间：2026-03-03 01:30*
