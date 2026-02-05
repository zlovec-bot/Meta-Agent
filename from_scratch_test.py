"""
从零生成 Agent 测试 - 用于对比实验
"""
from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv

load_dotenv()


def test_from_scratch():
    """测试从零生成 Agent 的方式"""
    client = ZhipuAI(api_key=os.getenv("GLM_API_KEY"))
    
    prompt = """
请创建一个完整的 Python Agent 代码，要求：
1. 能够搜索网络
2. 能够总结信息
3. 支持多轮对话
4. 使用 GLM-4 模型

请提供完整的代码实现，包括：
- 主程序文件
- 工具定义
- 配置文件
"""
    
    print("="*60)
    print("从零生成 Agent 测试")
    print("="*60)
    print(f"\n提示词：\n{prompt}\n")
    print("正在调用 GLM-4 生成代码...\n")
    
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    result = response.choices[0].message.content
    
    print("="*60)
    print("生成结果：")
    print("="*60)
    print(result)
    
    # 保存结果
    output_file = "from_scratch_result.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 从零生成 Agent 结果\n\n")
        f.write(f"## 提示词\n\n{prompt}\n\n")
        f.write(f"## 生成的代码\n\n{result}\n")
    
    print(f"\n结果已保存到: {output_file}")
    
    return result


if __name__ == "__main__":
    if not os.getenv("GLM_API_KEY"):
        print("❌ 错误：未设置 GLM_API_KEY")
        print("请在 .env 文件中配置你的智谱 AI API 密钥")
    else:
        test_from_scratch()
