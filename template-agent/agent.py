"""
标准 Agent 实现 - 使用 GLM-4 API
"""
import json
from zhipuai import ZhipuAI
from config import GLM_API_KEY, GLM_MODEL, MAX_ITERATIONS, TEMPERATURE
from tools import get_tool_definitions, execute_tool


class Agent:
    def __init__(self, system_prompt="你是一个有用的 AI 助手。"):
        self.client = ZhipuAI(api_key=GLM_API_KEY)
        self.model = GLM_MODEL
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
        """调用 GLM-4 API"""
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
    
    print("=== Template Agent ===")
    print("输入 '退出' 或 'quit' 结束对话\n")
    
    while True:
        # 获取用户输入
        user_input = input("用户: ").strip()
        
        # 检查是否退出
        if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
            print("再见！")
            break
            
        # 检查空输入
        if not user_input:
            print("请输入有效内容")
            continue
        
        # 运行 Agent
        response = agent.run(user_input)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
