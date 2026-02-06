# Meta-Agent 实验项目 (GLM-4 版本)

能创造 Agent 的 Agent - 使用智谱 AI GLM-4 模型

## 项目概述

本项目实现了一个具备元编程能力的 Coding Agent，能够根据用户需求自动创建新的 Agent 系统。通过"基于范例的代码生成"方法，确保生成的 Agent 遵循最佳实践。

## 项目结构

```
meta-agent-experiment/
├── template-agent/          # 范例 Agent（使用 GLM-4）
│   ├── agent.py            # Agent 主程序
│   ├── tools.py            # 工具定义
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # 依赖
│   └── .env.example        # 环境配置示例
├── meta-agent/             # Meta-Agent（能创建其他 Agent）
│   ├── meta_agent.py       # Meta-Agent 主程序
│   ├── meta_tools.py       # Meta-Agent 工具
│   ├── meta_config.py      # Meta-Agent 配置
│   ├── batch_test.py       # 批量测试脚本
│   ├── demo.py             # 演示脚本
│   ├── requirements.txt    # 依赖
│   └── .env.example        # 环境配置示例
├── generated-agents/       # 生成的 Agent（自动创建）
└── README.md              # 本文件
```

## 快速开始

### 1. 环境准备

```bash
# 安装 Python 3.9+
python --version

# 获取智谱 AI API 密钥
# 访问：https://open.bigmodel.cn/
```

### 2. 测试范例 Agent

```bash
# 进入范例 Agent 目录
cd template-agent

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# Windows 用户注意：如果 pyaudio 安装失败，请使用以下命令
pip install pipwin
pipwin install pyaudio

# 或者跳过 pyaudio（将无法使用语音功能）
# pip install zhipuai python-dotenv requests duckduckgo-search pyttsx3 SpeechRecognition

# 配置 API 密钥
copy .env.example .env
# 编辑 .env 文件，填入你的 GLM_API_KEY

# 运行测试
python agent.py
```

### 3. 运行 Meta-Agent

```bash
# 返回项目根目录
cd ..

# 进入 Meta-Agent 目录
cd meta-agent

# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
copy .env.example .env
# 编辑 .env 文件，填入你的 GLM_API_KEY

# 运行交互式演示（推荐）
python demo.py

# ⚠️ 注意：不要直接运行 python meta_agent.py
# 这会使用硬编码的需求，可能覆盖已生成的 agent
```

## 使用示例

### 创建自定义 Agent

运行 `demo.py` 并输入你的需求：

```bash
cd meta-agent
python demo.py
```

然后输入需求示例：

```
创建一个数据分析 Agent。

功能要求：
1. 能够读取 CSV 文件
2. 进行基本的统计分析
3. 生成分析报告

Agent 名称：data-analysis-agent
```

生成的 Agent 会保存在 `generated-agents/data-analysis-agent/` 目录

### 批量测试

```bash
cd meta-agent
python batch_test.py
```

## 核心特性

- ✅ 使用智谱 AI GLM-4 模型
- ✅ 标准的 Tool Calling 协议
- ✅ 基于范例的代码生成
- ✅ 自动化项目结构创建
- ✅ 完整的错误处理
- ✅ 中文注释和文档

## API 密钥配置

在 `.env` 文件中配置：

```bash
GLM_API_KEY=your-api-key-here
```

获取 API 密钥：
1. 访问 https://open.bigmodel.cn/
2. 注册/登录账号
3. 在控制台创建 API 密钥

## 常见问题

**Q: 如何获取 GLM API 密钥？**
A: 访问 https://open.bigmodel.cn/ 注册并在控制台创建密钥。

**Q: 生成的 Agent 无法运行？**
A: 检查 API 密钥配置、依赖安装和 Python 版本（需要 3.9+）。

**Q: 如何修改范例 Agent？**
A: 直接编辑 `template-agent/` 目录下的文件，Meta-Agent 会自动使用最新版本。

**Q: 如何避免覆盖已生成的 Agent？**
A: 始终使用 `python demo.py` 运行，并为每个 Agent 指定不同的名称。避免直接运行 `meta_agent.py`。

**Q: 网络搜索功能无法使用？**
A: 确保已安装 duckduckgo-search 库：`pip install duckduckgo-search>=5.0.0`。如果仍有问题，检查网络连接和防火墙设置。

**Q: pyaudio 安装失败怎么办？**
A: Windows 用户推荐使用 `pipwin install pyaudio` 或下载预编译的 wheel 文件。详见"依赖库说明"部分。如果不需要语音功能，可以跳过 pyaudio 安装。

**Q: 语音识别功能需要联网吗？**
A: 是的。`speech_to_text` 使用 Google Speech Recognition API，需要网络连接。`text_to_speech` 是离线的，不需要联网。

**Q: 如何测试语音功能是否正常？**
A: 运行 template-agent 后，输入"打开语音"或"语音对话"，系统会开始监听麦克风。如果能正常识别并朗读回复，说明功能正常。

**Q: 麦克风无法识别语音？**
A: 
1. 检查麦克风是否正常工作（在系统设置中测试）
2. 确认 pyaudio 已正确安装
3. 检查防火墙是否阻止了 Python 访问麦克风
4. 尝试增加 `speech_to_text` 的 timeout 参数

## 技术栈

- Python 3.9+
- 智谱 AI GLM-4 模型
- zhipuai SDK
- python-dotenv
- duckduckgo-search (网络搜索功能)

## 依赖库说明

### 核心依赖
- **zhipuai** (>=2.0.0): 智谱 AI SDK，用于调用 GLM-4 模型
- **python-dotenv** (>=1.0.0): 环境变量管理
- **requests** (>=2.31.0): HTTP 请求库

### 功能依赖
- **duckduckgo-search** (>=5.0.0): 网络搜索功能
- **pyttsx3**: 离线文字转语音（TTS）
- **SpeechRecognition**: 语音识别框架
- **pyaudio**: 音频输入/输出，麦克风支持

### 安装说明

#### 标准安装（Linux/macOS）
```bash
pip install -r requirements.txt
```

#### Windows 安装指南

**常规依赖**（通常无问题）：
```bash
pip install zhipuai python-dotenv requests duckduckgo-search pyttsx3 SpeechRecognition
```

**pyaudio 安装**（Windows 用户特别注意）：

pyaudio 在 Windows 上可能遇到编译错误：
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**解决方案 1：使用 pipwin（推荐）**
```bash
pip install pipwin
pipwin install pyaudio
```

**解决方案 2：使用预编译 wheel 文件**
```bash
# 1. 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# 2. 下载对应 Python 版本的 .whl 文件
#    例如：PyAudio-0.2.11-cp39-cp39-win_amd64.whl (Python 3.9, 64位)
# 3. 安装下载的文件
pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```

**解决方案 3：安装 Visual C++ 构建工具**
```bash
# 下载并安装 Microsoft C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
# 然后再执行：
pip install pyaudio
```

**验证安装**：
```python
# 测试 pyaudio 是否安装成功
python -c "import pyaudio; print('pyaudio 安装成功')"
```

### 可选：跳过语音功能

如果不需要语音交互功能，可以跳过 pyaudio 安装：
```bash
# 安装除 pyaudio 外的所有依赖
pip install zhipuai python-dotenv requests duckduckgo-search pyttsx3 SpeechRecognition
```

注意：跳过 pyaudio 后，`speech_to_text` 工具将无法使用，但其他功能正常。

## 许可证

MIT License
