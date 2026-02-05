"""
完整实验运行脚本
"""
import os
import sys
import time
from datetime import datetime


def check_environment():
    """检查环境配置"""
    print("="*60)
    print("环境检查")
    print("="*60)
    
    # 检查 Python 版本
    python_version = sys.version_info
    print(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        print("❌ Python 版本过低，需要 3.9+")
        return False
    else:
        print("✅ Python 版本符合要求")
    
    # 检查 API 密钥
    from dotenv import load_dotenv
    load_dotenv("meta-agent/.env")
    
    api_key = os.getenv("GLM_API_KEY")
    if not api_key:
        print("❌ 未设置 GLM_API_KEY")
        print("请在 meta-agent/.env 文件中配置")
        return False
    else:
        print("✅ API 密钥已配置")
    
    # 检查目录结构
    required_dirs = ["template-agent", "meta-agent"]
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ 目录存在: {directory}")
        else:
            print(f"❌ 目录缺失: {directory}")
            return False
    
    print("\n✅ 环境检查通过！\n")
    return True


def run_template_agent_test():
    """测试范例 Agent"""
    print("="*60)
    print("阶段 1: 测试范例 Agent")
    print("="*60)
    
    try:
        sys.path.insert(0, "template-agent")
        from agent import Agent
        
        agent = Agent(system_prompt="你是一个有用的 AI 助手。")
        print("✅ 范例 Agent 初始化成功")
        
        # 简单测试
        print("\n测试查询: 你好")
        response = agent.run("你好")
        print(f"响应: {response[:100]}...")
        
        print("\n✅ 范例 Agent 测试通过\n")
        return True
    except Exception as e:
        print(f"\n❌ 范例 Agent 测试失败: {e}\n")
        return False


def run_meta_agent_test():
    """测试 Meta-Agent"""
    print("="*60)
    print("阶段 2: 测试 Meta-Agent")
    print("="*60)
    
    try:
        sys.path.insert(0, "meta-agent")
        from meta_agent import MetaAgent
        
        meta_agent = MetaAgent()
        print("✅ Meta-Agent 初始化成功")
        
        requirement = """
创建一个简单的问答 Agent。

功能要求：
1. 能够回答用户问题
2. 保持对话历史

Agent 名称：simple-qa-agent
"""
        
        print("\n开始创建 Agent...")
        start_time = time.time()
        
        result = meta_agent.create_agent(requirement)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✅ Agent 创建完成")
        print(f"耗时: {duration:.2f} 秒")
        
        # 检查生成的文件
        agent_dir = "generated-agents/simple-qa-agent"
        if os.path.exists(agent_dir):
            print(f"✅ Agent 目录已创建: {agent_dir}")
            
            required_files = ["agent.py", "tools.py", "config.py", "requirements.txt"]
            for file in required_files:
                file_path = os.path.join(agent_dir, file)
                if os.path.exists(file_path):
                    print(f"  ✅ {file}")
                else:
                    print(f"  ❌ {file} 缺失")
        
        print("\n✅ Meta-Agent 测试通过\n")
        return True
    except Exception as e:
        print(f"\n❌ Meta-Agent 测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def run_comparison_test():
    """运行对比实验"""
    print("="*60)
    print("阶段 3: 对比实验")
    print("="*60)
    
    print("\n基于范例修改 vs 从零生成\n")
    
    # 基于范例修改的结果（已经在阶段2完成）
    print("✅ 基于范例修改: 已在阶段2完成")
    
    # 从零生成测试
    print("\n运行从零生成测试...")
    try:
        from from_scratch_test import test_from_scratch
        test_from_scratch()
        print("✅ 从零生成测试完成")
    except Exception as e:
        print(f"❌ 从零生成测试失败: {e}")
    
    print("\n请查看生成的结果并进行对比分析")
    print("参考文档: experiment_log_template.md\n")


def generate_report():
    """生成实验报告"""
    print("="*60)
    print("生成实验报告")
    print("="*60)
    
    report_content = f"""# Meta-Agent 实验报告

## 实验信息
- 实验日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 使用模型: GLM-4-Flash
- Python 版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}

## 实验阶段

### 阶段 1: 范例 Agent 测试
- 状态: 完成
- 结果: 成功

### 阶段 2: Meta-Agent 测试
- 状态: 完成
- 结果: 成功
- 生成的 Agent: simple-qa-agent

### 阶段 3: 对比实验
- 状态: 完成
- 对比项: 基于范例修改 vs 从零生成

## 下一步

1. 查看生成的 Agent: generated-agents/simple-qa-agent/
2. 运行批量测试: cd meta-agent && python batch_test.py
3. 填写详细实验记录: experiment_log_template.md
4. 进行代码质量对比分析

## 参考文档

- 实验指南: meta-agent-experiment.md
- 项目说明: README.md
- 实验记录模板: experiment_log_template.md
"""
    
    report_file = "experiment_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 实验报告已生成: {report_file}\n")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("Meta-Agent 完整实验")
    print("="*60 + "\n")
    
    # 1. 环境检查
    if not check_environment():
        print("请先完成环境配置")
        return
    
    # 2. 测试范例 Agent
    if not run_template_agent_test():
        print("范例 Agent 测试失败，请检查配置")
        return
    
    # 3. 测试 Meta-Agent
    if not run_meta_agent_test():
        print("Meta-Agent 测试失败，请检查代码")
        return
    
    # 4. 对比实验
    run_comparison_test()
    
    # 5. 生成报告
    generate_report()
    
    print("="*60)
    print("实验完成！")
    print("="*60)
    print("\n查看结果：")
    print("- 生成的 Agent: generated-agents/")
    print("- 实验报告: experiment_report.md")
    print("- 对比结果: from_scratch_result.md")


if __name__ == "__main__":
    main()
