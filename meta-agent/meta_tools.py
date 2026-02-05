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
# 编辑 .env 文件，填入你的 GLM API 密钥

# 运行 Agent
python agent.py
```

## 配置说明
在 `.env` 文件中配置你的智谱 AI API 密钥：
```
GLM_API_KEY=your-api-key-here
```

获取 API 密钥：https://open.bigmodel.cn/
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
