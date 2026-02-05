# Meta-Agent 实验项目 (GLM-4 版本)

能创造 Agent 的 Agent - 使用智谱 AI GLM-4 模型

## 项目概述

本项目实现了一个具备元编程能力的 Coding Agent，能够根据用户需求自动创建新的 Agent 系统。通过"基于范例的代码生成"方法，确保生成的 Agent 遵循最佳实践。

## 项目结构

```
meta-agent-experiment/
├── template-agent/          # 范例 Agent（使用 GLM-4）
│   ├── agent.py            # Agent 主程序
│   ├── tools.py            # 工具定义
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # 依赖
│   └── .env.example        # 环境配置示例
├── meta-agent/             # Meta-Agent（能创建其他 Agent）
│   ├── meta_agent.py       # Meta-Agent 主程序
│   ├── meta_tools.py       # Meta-Agent 工具
│   ├── meta_config.py      # Meta-Agent 配置
│   ├── batch_test.py       # 批量测试脚本
│   ├── demo.py             # 演示脚本
│   ├── requirements.txt    # 依赖
│   └── .env.example        # 环境配置示例
├── generated-agents/       # 生成的 Agent（自动创建）
└── README.md              # 本文件
```

## 快速开始

### 1. 环境准备

```bash
# 安装 Python 3.9+
python --version

# 获取智谱 AI API 密钥
# 访问：https://open.bigmodel.cn/
```

### 2. 测试范例 Agent

```bash
# 进入范例 Agent 目录
cd template-agent

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 注意：项目使用 DuckDuckGo Search (duckduckgo-search) 进行网络搜索
# 如果安装失败，可以单独安装：
# pip install duckduckgo-search>=5.0.0

# 配置 API 密钥
copy .env.example .env
# 编辑 .env 文件，填入你的 GLM_API_KEY

# 运行测试
python agent.py
```

### 3. 运行 Meta-Agent

```bash
# 返回项目根目录
cd ..

# 进入 Meta-Agent 目录
cd meta-agent

# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
copy .env.example .env
# 编辑 .env 文件，填入你的 GLM_API_KEY

# 运行交互式演示（推荐）
python demo.py

# ⚠️ 注意：不要直接运行 python meta_agent.py
# 这会使用硬编码的需求，可能覆盖已生成的 agent
```

## 使用示例

### 创建自定义 Agent

运行 `demo.py` 并输入你的需求：

```bash
cd meta-agent
python demo.py
```

然后输入需求示例：

```
创建一个数据分析 Agent。

功能要求：
1. 能够读取 CSV 文件
2. 进行基本的统计分析
3. 生成分析报告

Agent 名称：data-analysis-agent
```

生成的 Agent 会保存在 `generated-agents/data-analysis-agent/` 目录

### 批量测试

```bash
cd meta-agent
python batch_test.py
```

## 核心特性

- ✅ 使用智谱 AI GLM-4 模型
- ✅ 标准的 Tool Calling 协议
- ✅ 基于范例的代码生成
- ✅ 自动化项目结构创建
- ✅ 完整的错误处理
- ✅ 中文注释和文档

## API 密钥配置

在 `.env` 文件中配置：

```bash
GLM_API_KEY=your-api-key-here
```

获取 API 密钥：
1. 访问 https://open.bigmodel.cn/
2. 注册/登录账号
3. 在控制台创建 API 密钥

## 常见问题

**Q: 如何获取 GLM API 密钥？**
A: 访问 https://open.bigmodel.cn/ 注册并在控制台创建密钥。

**Q: 生成的 Agent 无法运行？**
A: 检查 API 密钥配置、依赖安装和 Python 版本（需要 3.9+）。

**Q: 如何修改范例 Agent？**
A: 直接编辑 `template-agent/` 目录下的文件，Meta-Agent 会自动使用最新版本。

**Q: 如何避免覆盖已生成的 Agent？**
A: 始终使用 `python demo.py` 运行，并为每个 Agent 指定不同的名称。避免直接运行 `meta_agent.py`。

**Q: 网络搜索功能无法使用？**
A: 确保已安装 duckduckgo-search 库：`pip install duckduckgo-search>=5.0.0`。如果仍有问题，检查网络连接和防火墙设置。

## 技术栈

- Python 3.9+
- 智谱 AI GLM-4 模型
- zhipuai SDK
- python-dotenv
- duckduckgo-search (网络搜索功能)

## 许可证

MIT License
