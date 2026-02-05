"""
Meta-Agent - 能够创建其他 Agent 的 Agent (使用 GLM-4)
"""
import json
from zhipuai import ZhipuAI
from meta_config import GLM_API_KEY, META_MODEL
from meta_tools import get_meta_tool_definitions, execute_meta_tool


class MetaAgent:
    def __init__(self):
        self.client = ZhipuAI(api_key=GLM_API_KEY)
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
- 保持代码使用 GLM-4 API 格式
- 使用智谱 AI 的 Tool Calling 协议
- 保持良好的错误处理和日志记录
- 确保生成的代码可以直接运行
- 所有代码使用中文注释
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
                assistant_message = {
                    "role": "assistant",
                    "content": response.choices[0].message.content or ""
                }
                
                # 添加工具调用信息
                if tool_calls:
                    assistant_message["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in tool_calls
                    ]
                
                self.conversation_history.append(assistant_message)
                
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
        """调用 GLM-4 API"""
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
