"""
票务查询工具 - 使用网络搜索获取真实信息
"""
from datetime import datetime, timedelta
from ddgs import DDGS


def get_tool_definitions():
    return [
        {
            "type": "function",
            "function": {
                "name": "search_tickets",
                "description": "搜索交通票务信息（高铁、火车、飞机），通过网络搜索获取真实的票务信息和购票链接",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "departure_city": {
                            "type": "string",
                            "description": "出发城市"
                        },
                        "destination_city": {
                            "type": "string",
                            "description": "目的地城市"
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "出发日期，格式：YYYY-MM-DD。如果用户说'明天'，请计算明天的日期"
                        },
                        "transport_type": {
                            "type": "string",
                            "description": "交通工具类型：train(火车/高铁) 或 flight(飞机)",
                            "enum": ["train", "flight"]
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "返回结果数量",
                            "default": 5
                        }
                    },
                    "required": ["departure_city", "destination_city", "departure_date", "transport_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_date",
                "description": "计算相对日期，例如'明天'、'后天'、'下周一'等",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relative_date": {
                            "type": "string",
                            "description": "相对日期描述，如：明天、后天、下周一"
                        }
                    },
                    "required": ["relative_date"]
                }
            }
        }
    ]


def execute_tool(tool_name, arguments):
    if tool_name == "search_tickets":
        return search_tickets(**arguments)
    elif tool_name == "calculate_date":
        return calculate_date(**arguments)
    else:
        return {"error": f"未知工具: {tool_name}"}


def calculate_date(relative_date):
    """计算相对日期"""
    try:
        today = datetime.now()
        
        if "明天" in relative_date or "明日" in relative_date:
            target_date = today + timedelta(days=1)
        elif "后天" in relative_date:
            target_date = today + timedelta(days=2)
        elif "今天" in relative_date or "今日" in relative_date:
            target_date = today
        else:
            # 默认返回明天
            target_date = today + timedelta(days=1)
        
        return {
            "success": True,
            "date": target_date.strftime("%Y-%m-%d"),
            "formatted": target_date.strftime("%Y年%m月%d日"),
            "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][target_date.weekday()]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_tickets(departure_city, destination_city, departure_date, transport_type="train", num_results=5):
    """通过网络搜索获取真实票务信息"""
    
    try:
        # 构建搜索查询
        transport_name = "高铁" if transport_type == "train" else "飞机"
        query = f"{departure_date} {departure_city}到{destination_city} {transport_name}票 时刻表 价格"
        
        print(f"[INFO] 搜索查询: {query}")
        
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=num_results))
        
        print(f"[DEBUG] 搜索到 {len(results)} 条结果")
        
        if not results:
            return {
                "success": False,
                "error": "未找到相关票务信息，建议直接访问 12306.cn 或携程、去哪儿等票务网站查询"
            }
        
        # 返回搜索结果
        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r.get("title", "无标题"),
                "description": r.get("body", "无描述"),
                "url": r.get("href", "")
            })
        
        return {
            "success": True,
            "query": {
                "from": departure_city,
                "to": destination_city,
                "date": departure_date,
                "type": transport_name
            },
            "note": "以下是从网络搜索获取的真实信息，请访问链接查看详细票务信息和购票",
            "count": len(formatted_results),
            "results": formatted_results
        }
        
    except Exception as e:
        print(f"[ERROR] 搜索失败: {str(e)}")
        return {
            "success": False,
            "error": f"搜索失败: {str(e)}，建议直接访问 12306.cn 查询"
        }
