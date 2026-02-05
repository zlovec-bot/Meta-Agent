# 能创造 Agent 的 Agent - 完整实验指南

## 实验概述

本实验构建一个具备元编程能力的 Coding Agent，使其能够根据用户需求自动创建新的 Agent 系统。通过"基于范例的代码生成"方法，确保生成的 Agent 遵循最佳实践。

## 实验环境准备

### 系统要求
- Python 3.9+
- Node.js 16+ (可选，用于 TypeScript 实现)
- Git
- 文本编辑器或 IDE

### API 密钥准备
```bash
# 需要至少一个 LLM API 密钥
export OPENAI_API_KEY="your-openai-key"
# 或
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## 第一阶段：创建高质量 Agent 范例

### 1.1 创建项目结构

```bash
# 创建项目根目录
mkdir meta-agent-experiment
cd meta-agent-experiment

# 创建范例 Agent 目录
mkdir -p template-agent
cd template-agent
```

### 1.2 创建范例 Agent 代码

#### 依赖管理文件 (requirements.txt)
```txt
openai>=1.12.0
anthropic>=0.18.0
python-dotenv>=1.0.0
requests>=2.31.0
```

#### 配置文件 (config.py)
```python
"""
Agent 配置文件 - 使用最新的 API 和最佳实践
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 模型配置 - 使用当前推荐的 SOTA 模型
OPENAI_MODEL = "gpt-4o"  # 2024 年最新模型
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"  # Claude 3.5 Sonnet

# API 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Agent 行为配置
MAX_ITERATIONS = 10
TEMPERATURE = 0.7
MAX_TOKENS = 4096
```

#### 工具定义 (tools.py)
```python
"""
标准工具定义 - 遵循 OpenAI Tool Calling 协议
"""

def get_tool_definitions():
    """返回符合 OpenAI Tool Calling 格式的工具定义"""
    return [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "搜索互联网获取最新信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询关键词"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "返回结果数量",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取本地文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "文件路径"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "写入内容到文件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "要写入的内容"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        }
    ]


def execute_tool(tool_name, arguments):
    """执行工具调用"""
    if tool_name == "web_search":
        return web_search(arguments.get("query"), arguments.get("num_results", 5))
    elif tool_name == "read_file":
        return read_file(arguments.get("file_path"))
    elif tool_name == "write_file":
        return write_file(arguments.get("file_path"), arguments.get("content"))
    else:
        return {"error": f"未知工具: {tool_name}"}


def web_search(query, num_results=5):
    """模拟网络搜索"""
    import requests
    try:
        # 这里使用简化的搜索 API 示例
        # 实际应用中应该使用 Google Custom Search API 或 Bing Search API
        return {
            "success": True,
            "results": [
                {"title": f"搜索结果 {i+1}", "snippet": f"关于 '{query}' 的信息..."}
                for i in range(num_results)
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def read_file(file_path):
    """读取文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}


def write_file(file_path, content):
    """写入文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"success": True, "message": f"成功写入文件: {file_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

#### 主程序 (agent.py)
```python
"""
标准 Agent 实现 - 使用最新的 OpenAI Chat Completions API
"""
import json
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_ITERATIONS, TEMPERATURE
from tools import get_tool_definitions, execute_tool


class Agent:
    def __init__(self, system_prompt="你是一个有用的 AI 助手。"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.system_prompt = system_prompt
        self.conversation_history = []
        self.tools = get_tool_definitions()
        
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []
        
    def run(self, user_message):
        """运行 Agent 主循环"""
        # 添加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        iteration = 0
        while iteration < MAX_ITERATIONS:
            iteration += 1
            print(f"\n--- 迭代 {iteration} ---")
            
            # 调用 LLM
            response = self._call_llm()
            
            # 检查是否需要调用工具
            if response.choices[0].finish_reason == "tool_calls":
                tool_calls = response.choices[0].message.tool_calls
                
                # 添加助手消息到历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in tool_calls
                    ]
                })
                
                # 执行工具调用
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"调用工具: {tool_name}")
                    print(f"参数: {tool_args}")
                    
                    # 执行工具
                    tool_result = execute_tool(tool_name, tool_args)
                    
                    # 添加工具结果到历史
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result, ensure_ascii=False)
                    })
                    
            else:
                # 没有工具调用，返回最终响应
                final_response = response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                return final_response
                
        return "达到最大迭代次数"
    
    def _call_llm(self):
        """调用 LLM API"""
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            temperature=TEMPERATURE
        )
        
        return response


def main():
    """测试 Agent"""
    agent = Agent(system_prompt="你是一个有用的 AI 助手，可以搜索网络和操作文件。")
    
    # 测试对话
    user_input = "搜索一下 Python 最新版本的信息"
    print(f"用户: {user_input}")
    
    response = agent.run(user_input)
    print(f"\nAgent: {response}")


if __name__ == "__main__":
    main()
```

#### 环境配置文件 (.env.example)
```bash
# OpenAI API 密钥
OPENAI_API_KEY=sk-your-key-here

# Anthropic API 密钥 (可选)
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 1.3 安装依赖并测试范例 Agent

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
copy .env.example .env
# 编辑 .env 文件，填入你的 API 密钥

# 测试范例 Agent
python agent.py
```

**预期输出**：Agent 应该能够成功调用工具并返回响应。

## 第二阶段：创建元编程 Agent (Meta-Agent)

### 2.1 创建 Meta-Agent 目录

```bash
# 返回项目根目录
cd ..

# 创建 Meta-Agent 目录
mkdir meta-agent
cd meta-agent
```

### 2.2 创建 Meta-Agent 代码

#### Meta-Agent 配置 (meta_config.py)
```python
"""
Meta-Agent 配置
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 使用更强大的模型进行代码生成
META_MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 范例 Agent 路径
TEMPLATE_AGENT_PATH = "../template-agent"

# 生成的 Agent 输出目录
OUTPUT_DIR = "../generated-agents"
```

#### Meta-Agent 工具 (meta_tools.py)
```python
"""
Meta-Agent 专用工具
"""
import os
import shutil
import json


def get_meta_tool_definitions():
    """Meta-Agent 的工具定义"""
    return [
        {
            "type": "function",
            "function": {
                "name": "read_template_file",
                "description": "读取范例 Agent 的文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "文件名 (如 agent.py, tools.py, config.py)"
                        }
                    },
                    "required": ["file_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_agent_project",
                "description": "创建新的 Agent 项目结构",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_name": {
                            "type": "string",
                            "description": "Agent 名称 (用于目录名)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Agent 功能描述"
                        }
                    },
                    "required": ["agent_name", "description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "modify_agent_file",
                "description": "修改生成的 Agent 文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_name": {
                            "type": "string",
                            "description": "Agent 名称"
                        },
                        "file_name": {
                            "type": "string",
                            "description": "要修改的文件名"
                        },
                        "content": {
                            "type": "string",
                            "description": "新的文件内容"
                        }
                    },
                    "required": ["agent_name", "file_name", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_template_files",
                "description": "列出范例 Agent 的所有文件",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]


def execute_meta_tool(tool_name, arguments):
    """执行 Meta-Agent 工具"""
    if tool_name == "read_template_file":
        return read_template_file(arguments.get("file_name"))
    elif tool_name == "create_agent_project":
        return create_agent_project(
            arguments.get("agent_name"),
            arguments.get("description")
        )
    elif tool_name == "modify_agent_file":
        return modify_agent_file(
            arguments.get("agent_name"),
            arguments.get("file_name"),
            arguments.get("content")
        )
    elif tool_name == "list_template_files":
        return list_template_files()
    else:
        return {"error": f"未知工具: {tool_name}"}


def read_template_file(file_name):
    """读取范例文件"""
    from meta_config import TEMPLATE_AGENT_PATH
    
    try:
        file_path = os.path.join(TEMPLATE_AGENT_PATH, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            "success": True,
            "file_name": file_name,
            "content": content
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_agent_project(agent_name, description):
    """创建新的 Agent 项目"""
    from meta_config import TEMPLATE_AGENT_PATH, OUTPUT_DIR
    
    try:
        # 创建输出目录
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # 创建 Agent 目录
        agent_dir = os.path.join(OUTPUT_DIR, agent_name)
        
        # 复制范例代码
        if os.path.exists(agent_dir):
            shutil.rmtree(agent_dir)
        shutil.copytree(TEMPLATE_AGENT_PATH, agent_dir)
        
        # 创建 README
        readme_content = f"""# {agent_name}

## 描述
{description}

## 使用方法
```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
copy .env.example .env
# 编辑 .env 文件

# 运行 Agent
python agent.py
```
"""
        with open(os.path.join(agent_dir, "README.md"), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return {
            "success": True,
            "message": f"成功创建 Agent 项目: {agent_name}",
            "path": agent_dir
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def modify_agent_file(agent_name, file_name, content):
    """修改 Agent 文件"""
    from meta_config import OUTPUT_DIR
    
    try:
        agent_dir = os.path.join(OUTPUT_DIR, agent_name)
        file_path = os.path.join(agent_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "message": f"成功修改文件: {file_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_template_files():
    """列出范例文件"""
    from meta_config import TEMPLATE_AGENT_PATH
    
    try:
        files = []
        for item in os.listdir(TEMPLATE_AGENT_PATH):
            item_path = os.path.join(TEMPLATE_AGENT_PATH, item)
            if os.path.isfile(item_path):
                files.append(item)
        
        return {
            "success": True,
            "files": files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

#### Meta-Agent 主程序 (meta_agent.py)
```python
"""
Meta-Agent - 能够创建其他 Agent 的 Agent
"""
import json
from openai import OpenAI
from meta_config import OPENAI_API_KEY, META_MODEL
from meta_tools import get_meta_tool_definitions, execute_meta_tool


class MetaAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = META_MODEL
        self.system_prompt = """你是一个专业的 Agent 开发专家。你的任务是根据用户需求创建新的 Agent。

工作流程：
1. 首先使用 list_template_files 查看可用的范例文件
2. 使用 read_template_file 读取相关范例文件，理解其结构
3. 使用 create_agent_project 创建新的 Agent 项目（这会自动复制范例代码）
4. 根据用户需求，使用 modify_agent_file 修改必要的文件：
   - tools.py: 添加或修改工具定义
   - agent.py: 调整 Agent 行为和系统提示词
   - config.py: 如需要可以调整配置
   - requirements.txt: 如需要可以添加新的依赖

重要原则：
- 保持代码使用最新的 API 格式（OpenAI Tool Calling 协议）
- 使用推荐的模型（gpt-4o, claude-3-5-sonnet）
- 保持良好的错误处理和日志记录
- 确保生成的代码可以直接运行
"""
        self.conversation_history = []
        self.tools = get_meta_tool_definitions()
        
    def create_agent(self, user_requirement):
        """根据用户需求创建 Agent"""
        print(f"\n{'='*60}")
        print(f"开始创建 Agent")
        print(f"需求: {user_requirement}")
        print(f"{'='*60}\n")
        
        # 添加用户消息
        self.conversation_history.append({
            "role": "user",
            "content": f"请根据以下需求创建一个新的 Agent：\n\n{user_requirement}"
        })
        
        iteration = 0
        max_iterations = 15
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n--- 迭代 {iteration} ---")
            
            # 调用 LLM
            response = self._call_llm()
            
            # 检查是否需要调用工具
            if response.choices[0].finish_reason == "tool_calls":
                tool_calls = response.choices[0].message.tool_calls
                
                # 添加助手消息到历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in tool_calls
                    ]
                })
                
                # 执行工具调用
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 调用工具: {tool_name}")
                    print(f"   参数: {json.dumps(tool_args, ensure_ascii=False, indent=2)}")
                    
                    # 执行工具
                    tool_result = execute_meta_tool(tool_name, tool_args)
                    
                    # 打印结果（简化版）
                    if tool_result.get("success"):
                        print(f"   ✅ 成功")
                    else:
                        print(f"   ❌ 失败: {tool_result.get('error')}")
                    
                    # 添加工具结果到历史
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result, ensure_ascii=False)
                    })
                    
            else:
                # 没有工具调用，返回最终响应
                final_response = response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                
                print(f"\n{'='*60}")
                print(f"Agent 创建完成！")
                print(f"{'='*60}")
                print(f"\n{final_response}")
                
                return final_response
                
        return "达到最大迭代次数，Agent 可能未完全创建"
    
    def _call_llm(self):
        """调用 LLM API"""
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            temperature=0.7
        )
        
        return response


def main():
    """主函数 - 演示 Meta-Agent 使用"""
    meta_agent = MetaAgent()
    
    # 示例需求
    requirement = """
创建一个能够搜索网络并总结信息的 Agent。

功能要求：
1. 能够接收用户的搜索查询
2. 使用 web_search 工具搜索相关信息
3. 分析搜索结果并生成简洁的摘要
4. 支持多轮对话，可以根据用户反馈进一步搜索

Agent 名称：web-research-agent
"""
    
    # 创建 Agent
    result = meta_agent.create_agent(requirement)
    
    print("\n" + "="*60)
    print("实验完成！")
    print("="*60)


if __name__ == "__main__":
    main()
```

#### Meta-Agent 依赖 (requirements.txt)
```txt
openai>=1.12.0
python-dotenv>=1.0.0
```

### 2.3 运行 Meta-Agent

```bash
# 安装依赖
pip install -r requirements.txt

# 复制环境配置
copy .env.example .env
# 编辑 .env 文件，填入 API 密钥

# 运行 Meta-Agent
python meta_agent.py
```

## 第三阶段：测试生成的 Agent

### 3.1 验证生成的 Agent 结构

```bash
# 查看生成的 Agent
cd ../generated-agents/web-research-agent

# 检查文件结构
dir
```

**预期文件结构**：
```
web-research-agent/
├── agent.py          # 主程序
├── tools.py          # 工具定义
├── config.py         # 配置文件
├── requirements.txt  # 依赖
├── .env.example      # 环境配置示例
└── README.md         # 说明文档
```

### 3.2 代码质量检查

#### 检查点 1：消息格式
打开 `agent.py`，检查是否使用标准的 OpenAI Chat Completions API 格式：

```python
# ✅ 正确的格式
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
```

#### 检查点 2：工具调用协议
打开 `tools.py`，检查工具定义格式：

```python
# ✅ 正确的 Tool Calling 格式
{
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "...",
        "parameters": {
            "type": "object",
            "properties": {...},
            "required": [...]
        }
    }
}
```

#### 检查点 3：模型选择
打开 `config.py`，检查模型配置：

```python
# ✅ 使用推荐的最新模型
OPENAI_MODEL = "gpt-4o"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
```

#### 检查点 4：上下文管理
检查 `agent.py` 中的对话历史管理：

```python
# ✅ 正确的上下文管理
self.conversation_history = []  # 初始化
self.conversation_history.append(...)  # 添加消息
```

### 3.3 功能测试

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境
copy .env.example .env
# 编辑 .env 文件

# 运行生成的 Agent
python agent.py
```

**测试用例**：
1. 简单搜索：`"搜索 Python 3.12 的新特性"`
2. 多轮对话：先搜索，然后要求"详细说明第一个特性"
3. 错误处理：提供无效输入，检查错误处理

### 3.4 性能记录

创建测试记录表：

| 测试项 | 预期结果 | 实际结果 | 通过 |
|--------|----------|----------|------|
| 代码可运行 | 无语法错误 | | ✅/❌ |
| API 格式正确 | 使用最新格式 | | ✅/❌ |
| 工具调用成功 | 正确调用工具 | | ✅/❌ |
| 上下文管理 | 正确维护历史 | | ✅/❌ |
| 错误处理 | 优雅处理错误 | | ✅/❌ |

## 第四阶段：对比实验

### 4.1 从零生成模式测试

创建一个简单的提示词，让 LLM 从零生成 Agent：

```python
# 创建 from_scratch_test.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
请创建一个完整的 Python Agent 代码，要求：
1. 能够搜索网络
2. 能够总结信息
3. 支持多轮对话

请提供完整的代码实现。
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
```

### 4.2 对比分析

创建对比表格：

| 对比维度 | 基于范例修改 | 从零生成 |
|----------|--------------|----------|
| **API 格式** | ✅ 使用最新 Tool Calling | ❌ 可能使用旧的 Function Calling |
| **模型选择** | ✅ gpt-4o / claude-3-5-sonnet | ❌ 可能使用 gpt-3.5-turbo |
| **代码结构** | ✅ 清晰的模块化结构 | ⚠️ 可能混在一个文件 |
| **错误处理** | ✅ 完整的异常处理 | ⚠️ 可能缺少错误处理 |
| **上下文管理** | ✅ 正确的历史管理 | ⚠️ 可能有上下文泄漏 |
| **开发时间** | ~2-3 分钟 | ~5-10 分钟 |
| **一次成功率** | ~90% | ~50% |
| **代码质量** | 高 | 中等 |

### 4.3 记录实验数据

创建实验记录文件 `experiment_log.md`：

```markdown
# 实验记录

## 实验 1：基于范例修改
- 开始时间：2024-XX-XX XX:XX
- 结束时间：2024-XX-XX XX:XX
- 耗时：X 分钟
- 生成的代码行数：XXX
- 首次运行结果：成功/失败
- 调试次数：X
- 最终状态：成功/失败

## 实验 2：从零生成
- 开始时间：2024-XX-XX XX:XX
- 结束时间：2024-XX-XX XX:XX
- 耗时：X 分钟
- 生成的代码行数：XXX
- 首次运行结果：成功/失败
- 调试次数：X
- 最终状态：成功/失败

## 发现的问题
1. ...
2. ...

## 改进建议
1. ...
2. ...
```

## 第五阶段：扩展实验

### 5.1 创建不同类型的 Agent

测试 Meta-Agent 创建不同功能的 Agent：

```python
# 测试用例 1：数据分析 Agent
requirement_1 = """
创建一个数据分析 Agent，能够：
1. 读取 CSV 文件
2. 进行基本的统计分析
3. 生成可视化图表
4. 回答关于数据的问题

Agent 名称：data-analysis-agent
"""

# 测试用例 2：代码审查 Agent
requirement_2 = """
创建一个代码审查 Agent，能够：
1. 读取代码文件
2. 检查代码质量问题
3. 提供改进建议
4. 生成审查报告

Agent 名称：code-review-agent
"""

# 测试用例 3：文档生成 Agent
requirement_3 = """
创建一个文档生成 Agent，能够：
1. 分析代码结构
2. 提取函数和类的文档字符串
3. 生成 Markdown 格式的 API 文档
4. 支持多种编程语言

Agent 名称：doc-generator-agent
"""
```

### 5.2 批量测试脚本

创建 `batch_test.py`：

```python
"""
批量测试 Meta-Agent
"""
from meta_agent import MetaAgent
import time

test_cases = [
    {
        "name": "web-research-agent",
        "requirement": "创建一个能够搜索网络并总结信息的 Agent"
    },
    {
        "name": "data-analysis-agent",
        "requirement": "创建一个数据分析 Agent，能够读取 CSV 并进行统计分析"
    },
    {
        "name": "code-review-agent",
        "requirement": "创建一个代码审查 Agent，能够检查代码质量"
    }
]

results = []

for test_case in test_cases:
    print(f"\n{'='*60}")
    print(f"测试: {test_case['name']}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    meta_agent = MetaAgent()
    try:
        result = meta_agent.create_agent(test_case['requirement'])
        success = True
        error = None
    except Exception as e:
        success = False
        error = str(e)
    
    end_time = time.time()
    duration = end_time - start_time
    
    results.append({
        "name": test_case['name'],
        "success": success,
        "duration": duration,
        "error": error
    })
    
    print(f"\n结果: {'成功' if success else '失败'}")
    print(f"耗时: {duration:.2f} 秒")
    if error:
        print(f"错误: {error}")

# 打印汇总
print(f"\n{'='*60}")
print("测试汇总")
print(f"{'='*60}")
for result in results:
    status = "✅" if result['success'] else "❌"
    print(f"{status} {result['name']}: {result['duration']:.2f}s")
```

## 第六阶段：验收与总结

### 6.1 验收检查清单

- [ ] Meta-Agent 能够成功创建新的 Agent
- [ ] 生成的 Agent 代码可以直接运行
- [ ] 生成的代码使用标准的消息格式
- [ ] 生成的代码使用最新的 Tool Calling 协议
- [ ] 生成的代码使用推荐的模型（gpt-4o 等）
- [ ] 生成的 Agent 能够正确管理对话上下文
- [ ] 基于范例修改的成功率高于从零生成
- [ ] 基于范例修改的开发效率高于从零生成

### 6.2 生成实验报告

创建 `experiment_report.md`：

```markdown
# Meta-Agent 实验报告

## 实验概述
- 实验日期：YYYY-MM-DD
- 实验人员：[姓名]
- 实验目的：验证基于范例的 Agent 生成方法的有效性

## 实验结果

### 成功率对比
- 基于范例修改：X/Y (XX%)
- 从零生成：X/Y (XX%)

### 开发效率对比
- 基于范例修改：平均 X 分钟
- 从零生成：平均 X 分钟

### 代码质量对比
| 质量指标 | 基于范例 | 从零生成 |
|----------|----------|----------|
| API 格式正确性 | XX% | XX% |
| 模型选择合理性 | XX% | XX% |
| 代码结构清晰度 | X/10 | X/10 |
| 错误处理完整性 | XX% | XX% |

## 关键发现

### 优势
1. 基于范例的方法确保了代码质量的下限
2. 生成的代码使用最新的 API 和最佳实践
3. 开发效率显著提高

### 挑战
1. 需要维护高质量的范例代码
2. 范例代码需要随着技术更新而更新
3. 对于特殊需求可能需要更多定制

## 改进建议
1. ...
2. ...

## 结论
[总结实验结果和发现]
```

### 6.3 最终演示

准备演示脚本 `demo.py`：

```python
"""
Meta-Agent 完整演示
"""
from meta_agent import MetaAgent
import os

def demo():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          Meta-Agent 演示                                 ║
║          能创造 Agent 的 Agent                           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 检查环境
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误：未设置 OPENAI_API_KEY")
        return
    
    print("✅ 环境检查通过\n")
    
    # 创建 Meta-Agent
    print("📦 初始化 Meta-Agent...")
    meta_agent = MetaAgent()
    print("✅ Meta-Agent 就绪\n")
    
    # 用户需求
    requirement = input("请输入你想创建的 Agent 需求（或按回车使用默认示例）：\n")
    
    if not requirement.strip():
        requirement = """
创建一个能够搜索网络并总结信息的 Agent。

功能要求：
1. 能够接收用户的搜索查询
2. 使用 web_search 工具搜索相关信息
3. 分析搜索结果并生成简洁的摘要
4. 支持多轮对话

Agent 名称：web-research-agent
"""
    
    # 创建 Agent
    print("\n🚀 开始创建 Agent...\n")
    result = meta_agent.create_agent(requirement)
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("="*60)
    print("\n生成的 Agent 位于: generated-agents/ 目录")
    print("请查看生成的代码并测试运行。")

if __name__ == "__main__":
    demo()
```

## 附录

### A. 常见问题

**Q1: Meta-Agent 生成的代码无法运行怎么办？**
A: 检查以下几点：
1. API 密钥是否正确配置
2. 依赖是否完整安装
3. Python 版本是否符合要求（3.9+）

**Q2: 如何更新范例 Agent？**
A: 直接修改 `template-agent/` 目录下的文件，Meta-Agent 会自动使用最新的范例。

**Q3: 可以使用其他 LLM 提供商吗？**
A: 可以，修改 `config.py` 和 `agent.py` 中的 API 调用部分即可。

### B. 参考资源

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [Tool Calling 最佳实践](https://platform.openai.com/docs/guides/function-calling)

### C. 项目结构总览

```
meta-agent-experiment/
├── template-agent/          # 范例 Agent
│   ├── agent.py
│   ├── tools.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
├── meta-agent/              # Meta-Agent
│   ├── meta_agent.py
│   ├── meta_tools.py
│   ├── meta_config.py
│   ├── requirements.txt
│   ├── batch_test.py
│   └── demo.py
├── generated-agents/        # 生成的 Agent
│   ├── web-research-agent/
│   ├── data-analysis-agent/
│   └── ...
├── experiment_log.md        # 实验记录
└── experiment_report.md     # 实验报告
```

---

**实验完成标志**：
- ✅ 成功创建范例 Agent
- ✅ 成功创建 Meta-Agent
- ✅ Meta-Agent 能够生成新的 Agent
- ✅ 生成的 Agent 可以运行
- ✅ 完成对比实验
- ✅ 生成实验报告

祝实验顺利！🎉
