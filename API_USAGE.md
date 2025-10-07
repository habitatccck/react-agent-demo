# LangGraph API 使用指南

## 概述

这个项目提供了两种方式来调用 LangGraph 代理：

1. **LangGraph Studio UI** - 图形界面
2. **API 客户端** - 编程接口

## 快速开始

### 1. 启动 LangGraph 服务器

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动开发服务器
langgraph dev
```

服务器将在 `http://localhost:2024` 启动。

### 2. 配置环境变量

创建 `.env` 文件并添加必要的 API 密钥：

```bash
# 模型配置
MODEL=openai/gpt-4o-mini

# API 密钥
OPENAI_API_KEY=your-openai-api-key-here
TAVILY_API_KEY=your-tavily-api-key-here
```

### 3. 使用 API 客户端

#### 简单调用示例

```python
# 运行简单客户端
python src/api/simple_client.py
```

#### 完整功能客户端

```python
# 运行完整客户端
python src/api/main.py
```

## API 客户端功能

### LangGraphAPIClient 类

```python
from src.api.main import LangGraphAPIClient

# 创建客户端
client = LangGraphAPIClient(url="http://localhost:2024")

# 发送消息
response = await client.chat("你好，请介绍一下你自己")

# 获取线程列表
threads = await client.get_threads()
```

### 主要方法

1. **`chat(message, thread_id=None)`**

   - 发送消息到代理
   - 返回响应数据

2. **`get_threads()`**
   - 获取所有线程列表
   - 用于管理对话历史

## 使用场景

### 1. 简单对话

```python
await client.chat("什么是人工智能？")
```

### 2. 搜索功能

```python
await client.chat("请搜索最新的机器学习技术")
```

### 3. 多轮对话

```python
# 使用同一个线程ID进行多轮对话
thread_id = "your-thread-id"
await client.chat("第一个问题", thread_id)
await client.chat("基于刚才的回答，继续提问", thread_id)
```

## 错误处理

客户端包含完整的错误处理机制：

- 连接错误处理
- API 响应错误处理
- 超时处理

## 配置选项

### 环境变量

- `LANGGRAPH_API_URL`: LangGraph 服务器地址
- `MODEL`: 使用的模型
- `OPENAI_API_KEY`: OpenAI API 密钥
- `TAVILY_API_KEY`: Tavily 搜索 API 密钥

### 模型配置

支持的模型格式：

- `openai/gpt-4o-mini`
- `openai/gpt-4-turbo-preview`
- `anthropic/claude-3-5-sonnet-20240620`

## 故障排除

### 常见问题

1. **连接错误**

   - 确保 LangGraph 服务器正在运行
   - 检查服务器地址是否正确

2. **API 密钥错误**

   - 确保设置了正确的 API 密钥
   - 检查密钥是否有效

3. **模型调用失败**
   - 检查模型名称是否正确
   - 确保有足够的 API 配额

### 调试模式

启用详细日志输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 扩展功能

### 添加自定义工具

在 `src/react_agent/tools.py` 中添加新工具：

```python
async def custom_tool(param: str) -> str:
    """自定义工具"""
    # 实现你的逻辑
    return "结果"

TOOLS = [search, custom_tool]
```

### 修改系统提示

在 `src/react_agent/prompts.py` 中修改：

```python
SYSTEM_PROMPT = """你是一个专业的AI助手..."""
```

## 更多信息

- [LangGraph 文档](https://github.com/langchain-ai/langgraph)
- [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio)
- [LangChain 文档](https://python.langchain.com/)
