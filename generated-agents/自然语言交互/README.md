# 自然语言交互

## 描述
自然语言交互的 Agent

## 使用方法
```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
copy .env.example .env
# 编辑 .env 文件，填入你的 GLM API 密钥

# 运行 Agent
python agent.py
```

## 配置说明
在 `.env` 文件中配置你的智谱 AI API 密钥：
```
GLM_API_KEY=your-api-key-here
```

获取 API 密钥：https://open.bigmodel.cn/
