"""
批量测试 Meta-Agent (使用 GLM-4)
"""
from meta_agent import MetaAgent
import time


def batch_test():
    """批量测试不同类型的 Agent 创建"""
    test_cases = [
        {
            "name": "web-research-agent",
            "requirement": """创建一个能够搜索网络并总结信息的 Agent。
功能要求：
1. 能够接收用户的搜索查询
2. 使用 web_search 工具搜索相关信息
3. 分析搜索结果并生成简洁的摘要
4. 支持多轮对话

Agent 名称：web-research-agent"""
        },
        {
            "name": "data-analysis-agent",
            "requirement": """创建一个数据分析 Agent。
功能要求：
1. 能够读取 CSV 文件
2. 进行基本的统计分析
3. 回答关于数据的问题
4. 生成分析报告

Agent 名称：data-analysis-agent"""
        },
        {
            "name": "code-review-agent",
            "requirement": """创建一个代码审查 Agent。
功能要求：
1. 能够读取代码文件
2. 检查代码质量问题
3. 提供改进建议
4. 生成审查报告

Agent 名称：code-review-agent"""
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
            print(f"错误: {error}")
        
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
    
    # 打印汇总
    print(f"\n{'='*60}")
    print("测试汇总")
    print(f"{'='*60}")
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['name']}: {result['duration']:.2f}s")
    
    # 统计
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    print(f"\n成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    return results


if __name__ == "__main__":
    batch_test()
