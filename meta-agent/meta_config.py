"""
Meta-Agent 配置 - 使用 GLM-4 模型
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 使用 GLM-4 模型进行代码生成
META_MODEL = "glm-4-flash"  # 使用 GLM-4 Flash 进行快速生成
GLM_API_KEY = os.getenv("GLM_API_KEY")

# 范例 Agent 路径
TEMPLATE_AGENT_PATH = "../template-agent"

# 生成的 Agent 输出目录
OUTPUT_DIR = "../generated-agents"
