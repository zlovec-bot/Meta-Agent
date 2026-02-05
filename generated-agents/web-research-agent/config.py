"""
Agent 配置文件 - 使用 GLM-4 模型
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 模型配置 - 使用智谱 AI GLM-4
GLM_MODEL = "glm-4-flash"  # GLM-4 Flash 模型，速度快且性能好
GLM_API_KEY = os.getenv("GLM_API_KEY")

# Agent 行为配置
MAX_ITERATIONS = 10
TEMPERATURE = 0.7
MAX_TOKENS = 4096
