"""
项目安装脚本
"""
import os
import shutil


def setup_project():
    """设置项目环境"""
    print("="*60)
    print("Meta-Agent 项目设置")
    print("="*60)
    
    # 创建必要的目录
    directories = [
        "template-agent",
        "meta-agent",
        "generated-agents"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ 创建目录: {directory}")
        else:
            print(f"✓ 目录已存在: {directory}")
    
    # 复制环境配置文件
    env_files = [
        ("template-agent/.env.example", "template-agent/.env"),
        ("meta-agent/.env.example", "meta-agent/.env")
    ]
    
    for src, dst in env_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
            print(f"✅ 创建配置文件: {dst}")
        elif os.path.exists(dst):
            print(f"✓ 配置文件已存在: {dst}")
    
    print("\n" + "="*60)
    print("设置完成！")
    print("="*60)
    print("\n下一步：")
    print("1. 编辑 template-agent/.env 和 meta-agent/.env")
    print("2. 填入你的 GLM_API_KEY")
    print("3. 运行: cd meta-agent && python demo.py")
    print("\n获取 API 密钥：https://open.bigmodel.cn/")


if __name__ == "__main__":
    setup_project()
