"""
Meta-Agent 完整演示 (使用 GLM-4)
"""
from meta_agent import MetaAgent
import os


def demo():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          Meta-Agent 演示                                 ║
║          能创造 Agent 的 Agent (GLM-4)                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 检查环境
    if not os.getenv("GLM_API_KEY"):
        print("❌ 错误：未设置 GLM_API_KEY")
        print("请在 .env 文件中配置你的智谱 AI API 密钥")
        print("获取密钥：https://open.bigmodel.cn/")
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
