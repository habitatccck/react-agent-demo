# React Agent FastAPI 服务

基于 LangGraph 的 ReAct Agent，提供 FastAPI 接口服务。

## 特性

- 🤖 **ReAct Agent**: 推理和行动代理
- 🚀 **FastAPI**: 高性能 Web 框架
- 🐳 **Docker**: 容器化部署
- 🔍 **搜索功能**: 集成 Tavily 搜索
- 💬 **聊天接口**: RESTful API

## 快速开始

### 1. 环境准备

```bash
# 复制环境变量文件
cp env.example .env

# 编辑 .env 文件，设置 API 密钥
nano .env
```

**必需的环境变量**：

```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 2. 启动服务

#### 方式一：Docker 部署（推荐）

```bash
# 一键启动
./docker-run.sh

# 或手动启动
docker-compose up -d --build
```

#### 方式二：本地开发

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动服务
python start_direct_fastapi.py
```

### 3. 验证部署

```bash
# 健康检查
curl http://localhost:8000/api/health

# 测试聊天
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "conversation_id": "test"}'
```

## API 文档

- **服务地址**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/health

### 主要端点

| 端点                     | 方法   | 说明         |
| ------------------------ | ------ | ------------ |
| `/api/chat`              | POST   | 聊天对话     |
| `/api/chat/history/{id}` | GET    | 获取对话历史 |
| `/api/chat/history/{id}` | DELETE | 清除对话历史 |
| `/api/health`            | GET    | 健康检查     |

### 请求示例

```json
{
  "message": "请搜索今天的最新新闻",
  "conversation_id": "user123",
  "model": "openai/gpt-4o-mini",
  "max_search_results": 10
}
```

## 项目结构

```
├── src/
│   ├── api/
│   │   └── direct_fastapi_app.py    # FastAPI 应用
│   └── react_agent/
│       ├── graph.py                 # 图定义
│       ├── context.py              # 上下文配置
│       ├── state.py                # 状态定义
│       ├── tools.py                # 工具函数
│       └── utils.py                # 工具函数
├── Dockerfile                       # Docker 镜像
├── docker-compose.yml              # Docker 编排
├── start_direct_fastapi.py         # 启动脚本
└── docker-run.sh                   # Docker 运行脚本
```

## 开发说明

### 添加新工具

在 `src/react_agent/tools.py` 中添加新工具：

```python
async def new_tool(param: str) -> str:
    """新工具的描述"""
    # 工具逻辑
    return result

# 添加到工具列表
TOOLS = [search, new_tool]
```

### 自定义模型

在请求中指定模型：

```json
{
  "message": "你好",
  "model": "openai/gpt-4o-mini"
}
```

### 自定义提示词

修改 `src/react_agent/prompts.py`：

```python
SYSTEM_PROMPT = """你是一个专业的助手..."""
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 生产环境

```bash
# 使用 Gunicorn
gunicorn src.api.direct_fastapi_app:app -w 4 -k uvicorn.workers.UvicornWorker

# 使用 Nginx 反向代理
# 配置 nginx.conf
```

## Railway 云部署

### 快速部署到 Railway

1. **准备环境变量**

   ```bash
   # 复制环境变量示例
   cp env.example .env
   # 编辑 .env 文件设置 API 密钥
   ```

2. **部署到 Railway**

   ```bash
   # 安装 Railway CLI
   npm install -g @railway/cli

   # 登录并部署
   railway login
   railway init
   railway up
   ```

3. **设置环境变量**
   在 Railway 控制台设置以下环境变量：

   - `OPENAI_API_KEY`: 你的 OpenAI API 密钥
   - `TAVILY_API_KEY`: Tavily 搜索 API 密钥

4. **访问服务**
   Railway 会提供一个公网 URL，例如：
   ```
   https://your-app-name.railway.app
   ```

### Railway 部署特性

- ✅ **自动端口配置**: Railway 自动设置 `PORT` 环境变量
- ✅ **公网访问**: 自动获得公网 IP 和域名
- ✅ **健康检查**: 自动监控服务状态
- ✅ **日志监控**: 实时查看服务日志
- ✅ **自动重启**: 服务异常时自动重启

### 详细部署指南

查看 [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) 获取完整的部署指南。

## 故障排除

### 常见问题

1. **API 密钥错误**

   ```bash
   # 检查 .env 文件
   cat .env
   ```

2. **服务启动失败**

   ```bash
   # 查看日志
   docker-compose logs
   ```

3. **端口冲突**
   ```bash
   # 修改 docker-compose.yml 中的端口
   ports:
     - "8001:8000"
   ```

## 许可证

MIT License

python3 -m venv venv
source venv/bin/activate
pip install "langgraph-cli[inmem]"
pip install -e .

docker-compose build --no-cache

docker-compose up -d
