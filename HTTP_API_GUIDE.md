# LangGraph HTTP API 服务指南

## 概述

这个项目提供了一个 HTTP API 服务，封装了 LangGraph 代理调用，对外暴露 REST API 接口，供前端或其他服务调用。

## 快速开始

### 1. 启动 LangGraph 服务器

首先需要启动 LangGraph 开发服务器：

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动LangGraph服务器
langgraph dev
```

LangGraph 服务器将在 `http://localhost:2024` 启动。

### 2. 启动 HTTP API 服务

在另一个终端中启动 HTTP API 服务：

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动HTTP API服务
python start_api.py
```

HTTP API 服务将在 `http://localhost:8000` 启动。

### 3. 测试 API 服务

```bash
# 运行测试脚本
python test_api.py
```

## API 接口文档

### 基础信息

- **服务地址**: `http://localhost:8000`
- **API 文档**: `http://localhost:8000/docs`
- **健康检查**: `http://localhost:8000/health`

### 接口列表

#### 1. 健康检查

```http
GET /health
```

**响应示例**:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0"
}
```

#### 2. 聊天接口

```http
POST /api/chat
```

**请求体**:

```json
{
  "message": "你好，请介绍一下你自己",
  "thread_id": "optional-thread-id",
  "model": "optional-model-name"
}
```

**响应示例**:

```json
{
  "success": true,
  "message": "聊天请求处理成功",
  "data": {
    "response": "你好！我是一个AI助手...",
    "full_data": [...],
    "model_used": "default"
  },
  "thread_id": "thread-123",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 3. 获取线程列表

```http
GET /api/threads
```

**响应示例**:

```json
{
  "success": true,
  "data": [...],
  "message": "获取线程列表成功",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 4. 获取可用模型

```http
GET /api/models
```

**响应示例**:

```json
{
  "success": true,
  "data": {
    "models": [
      "openai/gpt-4o-mini",
      "openai/gpt-4-turbo-preview",
      "anthropic/claude-3-5-sonnet-20240620"
    ],
    "default": "openai/gpt-4o-mini"
  },
  "message": "获取模型列表成功",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 使用示例

### Python 客户端示例

```python
import requests

# 发送聊天请求
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "什么是人工智能？",
        "thread_id": None  # 创建新线程
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"AI回复: {data['data']['response']}")
    thread_id = data['thread_id']

    # 继续对话
    response2 = requests.post(
        "http://localhost:8000/api/chat",
        json={
            "message": "请详细解释一下",
            "thread_id": thread_id  # 使用同一个线程
        }
    )
```

### JavaScript 客户端示例

```javascript
// 发送聊天请求
async function chat(message, threadId = null) {
  const response = await fetch("http://localhost:8000/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: message,
      thread_id: threadId,
    }),
  });

  const data = await response.json();
  return data;
}

// 使用示例
chat("你好，请介绍一下你自己")
  .then((response) => {
    console.log("AI回复:", response.data.response);
    return chat("请详细说明", response.thread_id);
  })
  .then((response) => {
    console.log("AI回复:", response.data.response);
  });
```

### curl 示例

```bash
# 发送聊天请求
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是LangGraph？",
    "thread_id": null
  }'

# 健康检查
curl "http://localhost:8000/health"

# 获取线程列表
curl "http://localhost:8000/api/threads"
```

## 配置选项

### 环境变量

| 变量名              | 默认值                  | 描述                 |
| ------------------- | ----------------------- | -------------------- |
| `API_HOST`          | `0.0.0.0`               | HTTP 服务监听地址    |
| `API_PORT`          | `8000`                  | HTTP 服务端口        |
| `LANGGRAPH_API_URL` | `http://localhost:2024` | LangGraph 服务器地址 |

### 设置环境变量

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export LANGGRAPH_API_URL=http://localhost:2024
```

## 错误处理

### 常见错误码

- `200`: 成功
- `400`: 请求参数错误
- `500`: 服务器内部错误

### 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

## 部署说明

### 开发环境

```bash
# 启动LangGraph服务器
langgraph dev

# 启动HTTP API服务
python start_api.py
```

### 生产环境

```bash
# 使用gunicorn部署
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.http_service:app --bind 0.0.0.0:8000
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "start_api.py"]
```

## 监控和日志

### 健康检查

定期检查服务状态：

```bash
curl http://localhost:8000/health
```

### 日志查看

服务日志会显示在控制台，包括：

- 请求日志
- 错误日志
- LangGraph 调用日志

## 扩展功能

### 添加新的 API 接口

在 `src/api/http_service.py` 中添加新的路由：

```python
@app.post("/api/custom")
async def custom_endpoint(request: CustomRequest):
    # 实现自定义逻辑
    pass
```

### 添加中间件

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 故障排除

### 常见问题

1. **连接 LangGraph 服务器失败**

   - 确保 LangGraph 服务器正在运行
   - 检查 `LANGGRAPH_API_URL` 配置

2. **API 服务启动失败**

   - 检查端口是否被占用
   - 确保所有依赖已安装

3. **聊天请求超时**
   - 检查模型 API 密钥配置
   - 查看 LangGraph 服务器日志

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 更多信息

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [LangGraph 文档](https://github.com/langchain-ai/langgraph)
- [Uvicorn 文档](https://www.uvicorn.org/)
