"""
标准工具定义 - 遵循 GLM-4 Tool Calling 协议
"""
from ddgs import DDGS

def get_tool_definitions():
    """返回符合 GLM-4 Tool Calling 格式的工具定义"""
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
    """真实网络搜索 - 使用 DuckDuckGo"""
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=num_results))
        
        # 调试：打印原始结果
        print(f"[DEBUG] 搜索到 {len(results)} 条结果")
        
        if not results:
            return {
                "success": False, 
                "error": "未找到搜索结果，请尝试其他关键词"
            }
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r.get("title", "无标题"),
                "snippet": r.get("body", "无描述"),
                "url": r.get("href", "")
            })
        
        return {
            "success": True,
            "query": query,
            "count": len(formatted_results),
            "results": formatted_results
        }
    except Exception as e:
        print(f"[ERROR] 搜索失败: {str(e)}")
        return {"success": False, "error": f"搜索出错: {str(e)}"}


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
