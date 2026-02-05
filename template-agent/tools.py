"""
标准工具定义 - 遵循 GLM-4 Tool Calling 协议
"""
from ddgs import DDGS
import pyttsx3
import speech_recognition as sr

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
        },
        {
            "type": "function",
            "function": {
                "name": "text_to_speech",
                "description": "将文本转换为语音播放（离线TTS）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要朗读的文本内容"
                        },
                        "rate": {
                            "type": "integer",
                            "description": "语速，范围50-300，默认150",
                            "default": 150
                        },
                        "volume": {
                            "type": "number",
                            "description": "音量，范围0.0-1.0，默认1.0",
                            "default": 1.0
                        }
                    },
                    "required": ["text"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "speech_to_text",
                "description": "监听麦克风输入并将语音转换为文字。调用此工具后会进入语音对话模式，你需要用 text_to_speech 朗读回复",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timeout": {
                            "type": "integer",
                            "description": "监听超时时间（秒），默认5秒",
                            "default": 5
                        },
                        "language": {
                            "type": "string",
                            "description": "识别语言代码，如'zh-CN'(中文)、'en-US'(英文)，默认'zh-CN'",
                            "default": "zh-CN"
                        }
                    },
                    "required": []
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
    elif tool_name == "text_to_speech":
        return text_to_speech(
            arguments.get("text"),
            arguments.get("rate", 150),
            arguments.get("volume", 1.0)
        )
    elif tool_name == "speech_to_text":
        return speech_to_text(
            arguments.get("timeout", 5),
            arguments.get("language", "zh-CN")
        )
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


def text_to_speech(text, rate=150, volume=1.0):
    """文字转语音（TTS）- 离线实现"""
    try:
        engine = pyttsx3.init()
        
        # 设置语速
        engine.setProperty('rate', rate)
        
        # 设置音量
        engine.setProperty('volume', volume)
        
        # 播放语音
        print(f"[TTS] 正在播放: {text[:50]}{'...' if len(text) > 50 else ''}")
        engine.say(text)
        engine.runAndWait()
        
        return {
            "success": True,
            "message": f"已成功播放语音",
            "text": text,
            "rate": rate,
            "volume": volume
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"语音播放失败: {str(e)}"
        }


def speech_to_text(timeout=5, language="zh-CN"):
    """语音转文字（STT）"""
    try:
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print(f"[STT] 请说话... (超时时间: {timeout}秒)")
            
            # 调整环境噪音
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # 监听语音
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
        
        print("[STT] 正在识别...")
        
        # 使用 Google 语音识别（免费，需要网络）
        text = recognizer.recognize_google(audio, language=language)
        
        print(f"[STT] 识别结果: {text}")
        
        return {
            "success": True,
            "text": text,
            "language": language
        }
        
    except sr.WaitTimeoutError:
        return {
            "success": False,
            "error": "监听超时，未检测到语音输入"
        }
    except sr.UnknownValueError:
        return {
            "success": False,
            "error": "无法识别语音内容，请说清楚一些"
        }
    except sr.RequestError as e:
        return {
            "success": False,
            "error": f"语音识别服务错误: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"语音识别失败: {str(e)}"
        }
