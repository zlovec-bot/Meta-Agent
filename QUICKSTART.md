# 快速开始指南

## 一键运行实验

### Windows 系统

```bash
# 1. 克隆或下载项目
cd meta-agent-experiment

# 2. 安装依赖
pip install zhipuai python-dotenv requests

# 3. 配置 API 密钥
# 编辑 meta-agent/.env 文件
# 填入: GLM_API_KEY=your-api-key-here

# 4. 运行完整实验
python run_experiment.py
```

### 获取 API 密钥

1. 访问 https://open.bigmodel.cn/
2. 注册/登录账号
3. 进入控制台 → API 密钥
4. 创建新密钥并复制

### 分步运行

#### 步骤 1: 测试范例 Agent

```bash
cd template-agent
pip install -r requirements.txt
copy .env.example .env
# 编辑 .env 文件，填入 GLM_API_KEY
python agent.py
```

#### 步骤 2: 运行 Meta-Agent

```bash
cd ../meta-agent
pip install -r requirements.txt
copy .env.example .env
# 编辑 .env 文件，填入 GLM_API_KEY
python demo.py
```

#### 步骤 3: 批量测试

```bash
cd meta-agent
python batch_test.py
```

#### 步骤 4: 对比实验

```bash
cd ..
python from_scratch_test.py
```

## 验证安装

```bash
# 检查 Python 版本
python --version  # 需要 3.9+

# 检查依赖
pip list | findstr zhipuai

# 测试 API 连接
python -c "from zhipuai import ZhipuAI; import os; from dotenv import load_dotenv; load_dotenv('meta-agent/.env'); client = ZhipuAI(api_key=os.getenv('GLM_API_KEY')); print('✅ API 连接成功')"
```

## 常见问题

### 问题 1: ModuleNotFoundError: No module named 'zhipuai'

```bash
pip install zhipuai
```

### 问题 2: API 密钥错误

检查 `.env` 文件中的密钥是否正确：
```bash
GLM_API_KEY=your-actual-api-key-here
```

### 问题 3: 编码错误

确保文件使用 UTF-8 编码保存。

## 项目结构

```
meta-agent-experiment/
├── template-agent/          # 范例 Agent
├── meta-agent/              # Meta-Agent
├── generated-agents/        # 生成的 Agent（运行后创建）
├── run_experiment.py        # 完整实验脚本
├── from_scratch_test.py     # 对比实验脚本
├── README.md               # 项目说明
└── QUICKSTART.md           # 本文件
```

## 下一步

1. 查看生成的 Agent 代码
2. 修改需求创建自定义 Agent
3. 填写实验记录表格
4. 进行代码质量对比分析

## 获取帮助

- 查看详细文档: meta-agent-experiment.md
- 查看项目说明: README.md
- 智谱 AI 文档: https://open.bigmodel.cn/dev/api
