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
        self.voice_mode = False  # 语音模式标志
        
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []
        
    def run(self, user_message):
        """运行 Agent 主循环"""
        # 检测关闭语音命令
        if self.voice_mode and any(keyword in user_message for keyword in ["关闭语音", "退出语音", "停止语音"]):
            self.voice_mode = False
            print("[语音模式] 已关闭")
        
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
                    
                    # 检测语音模式切换并处理识别的文字
                    if tool_name == "speech_to_text" and tool_result.get("success"):
                        self.voice_mode = True
                        print("[语音模式] 已开启")
                        recognized_text = tool_result.get("text", "")
                        if recognized_text:
                            print(f"[语音输入] {recognized_text}")
                            # 将识别的文字作为新的用户消息添加到历史
                            self.conversation_history.append({
                                "role": "user",
                                "content": recognized_text
                            })
                    
            else:
                # 没有工具调用，返回最终响应
                final_response = response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                
                # 语音模式：朗读回复并继续监听
                if self.voice_mode:
                    print(f"\nAgent: {final_response}")
                    
                    # 朗读回复
                    tts_result = execute_tool("text_to_speech", {"text": final_response})
                    
                    if tts_result.get("success"):
                        # 朗读成功后，继续监听下一句话
                        print("\n[语音模式] 继续监听...")
                        stt_result = execute_tool("speech_to_text", {"language": "zh-CN", "timeout": 5})
                        
                        if stt_result.get("success"):
                            recognized_text = stt_result.get("text", "")
                            print(f"[语音输入] {recognized_text}")
                            
                            # 检测关闭语音命令
                            if any(keyword in recognized_text for keyword in ["关闭语音", "退出语音", "停止语音"]):
                                self.voice_mode = False
                                print("[语音模式] 已关闭")
                                return final_response
                            
                            # 递归处理新的语音输入
                            return self.run(recognized_text)
                        else:
                            # STT 失败，退出语音模式
                            print(f"[语音模式] 监听失败: {stt_result.get('error')}")
                            self.voice_mode = False
                
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
    agent = Agent(system_prompt="""你是一个有用的 AI 助手，可以搜索网络和操作文件。

语音交互规则：
1. 当用户说"打开语音"、"开启语音"、"语音对话"时，你必须立即调用 speech_to_text 工具来监听用户的语音输入
2. speech_to_text 工具会识别用户的语音并转换为文字，识别的文字会作为用户的新消息
3. 收到语音识别的文字后，你需要：
   - 理解用户说的内容并生成合适的回复
   - 调用 text_to_speech 工具朗读你的回复（不是朗读用户说的话）
   - 朗读完成后，立即再次调用 speech_to_text 继续监听下一句话
4. 在语音对话模式下，形成循环：监听 → 回复 → 朗读 → 再次监听
5. 如果用户说"关闭语音"、"退出语音"、"停止语音"，则不要再调用 speech_to_text，退出语音模式
6. 重要：语音模式下每次回复后都要自动继续监听，保持对话连续性！""")
    
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
