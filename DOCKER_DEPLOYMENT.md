# Docker 部署指南

## 概述

本指南介绍如何使用 Docker 部署 LangGraph HTTP API 服务。部署包含两个服务：

- **LangGraph 服务**: 大模型推理服务
- **HTTP API 服务**: REST API 接口服务

## 快速开始

### 1. 准备环境变量

```bash
# 复制环境变量模板
cp env.docker.example .env

# 编辑环境变量文件，填入真实的 API 密钥
nano .env
```

### 2. 构建和启动服务

```bash
# 构建并启动所有服务
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

### 3. 验证部署

```bash
# 检查服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f

# 测试 API 服务
curl http://localhost:8000/health

# 测试 LangGraph 服务
curl http://localhost:2024/health
```

## 服务架构

```
┌─────────────────┐    ┌─────────────────┐
│   HTTP API      │    │   LangGraph     │
│   Port: 8000    │◄──►│   Port: 2024    │
│                 │    │                 │
│ - /api/chat     │    │ - 模型推理      │
│ - /health       │    │ - 工具调用      │
│ - /docs         │    │ - 状态管理      │
└─────────────────┘    └─────────────────┘
```

## 详细配置

### 环境变量说明

| 变量名              | 默认值                  | 描述                 |
| ------------------- | ----------------------- | -------------------- |
| `MODEL`             | `openai/gpt-4o-mini`    | 使用的模型           |
| `OPENAI_API_KEY`    | -                       | OpenAI API 密钥      |
| `ANTHROPIC_API_KEY` | -                       | Anthropic API 密钥   |
| `TAVILY_API_KEY`    | -                       | Tavily 搜索 API 密钥 |
| `API_HOST`          | `0.0.0.0`               | HTTP API 监听地址    |
| `API_PORT`          | `8000`                  | HTTP API 端口        |
| `LANGGRAPH_API_URL` | `http://langgraph:2024` | LangGraph 服务地址   |

### 服务配置

#### LangGraph 服务

- **端口**: 2024
- **健康检查**: `http://localhost:2024/health`
- **重启策略**: `unless-stopped`
- **依赖**: 无

#### HTTP API 服务

- **端口**: 8000
- **健康检查**: `http://localhost:8000/health`
- **重启策略**: `unless-stopped`
- **依赖**: LangGraph 服务

## 部署选项

### 选项一：开发环境部署

```bash
# 启动开发环境（包含热重载）
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### 选项二：生产环境部署

```bash
# 启动生产环境
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### 选项三：单服务部署

```bash
# 只启动 HTTP API 服务（需要外部 LangGraph 服务）
docker-compose up api

# 只启动 LangGraph 服务
docker-compose up langgraph
```

## 管理命令

### 基本操作

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec [service_name] /bin/bash
```

### 服务管理

```bash
# 查看服务状态
docker-compose ps

# 查看服务资源使用
docker-compose top

# 重新构建服务
docker-compose build [service_name]

# 强制重新创建容器
docker-compose up --force-recreate
```

### 数据管理

```bash
# 查看数据卷
docker volume ls

# 备份数据
docker run --rm -v langgraph-data:/data -v $(pwd):/backup alpine tar czf /backup/langgraph-data.tar.gz -C /data .

# 恢复数据
docker run --rm -v langgraph-data:/data -v $(pwd):/backup alpine tar xzf /backup/langgraph-data.tar.gz -C /data
```

## 监控和日志

### 健康检查

```bash
# 检查 HTTP API 服务
curl http://localhost:8000/health

# 检查 LangGraph 服务
curl http://localhost:2024/health

# 检查所有服务
docker-compose ps
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api
docker-compose logs -f langgraph

# 查看最近的日志
docker-compose logs --tail=100 -f
```

### 性能监控

```bash
# 查看资源使用情况
docker stats

# 查看容器详细信息
docker inspect [container_name]

# 查看网络连接
docker network ls
docker network inspect langgraph-network
```

## 故障排除

### 常见问题

1. **服务启动失败**

   ```bash
   # 检查日志
   docker-compose logs [service_name]

   # 检查端口占用
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :2024
   ```

2. **API 密钥错误**

   ```bash
   # 检查环境变量
   docker-compose config

   # 重新设置环境变量
   docker-compose down
   docker-compose up --build
   ```

3. **网络连接问题**

   ```bash
   # 检查网络
   docker network ls
   docker network inspect langgraph-network

   # 重启网络
   docker-compose down
   docker-compose up
   ```

### 调试模式

```bash
# 启用调试日志
export DEBUG=1
docker-compose up

# 进入容器调试
docker-compose exec api /bin/bash
docker-compose exec langgraph /bin/bash
```

## 生产环境优化

### 性能优化

```yaml
# docker-compose.prod.yml
version: "3.8"
services:
  api:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
        reservations:
          cpus: "0.5"
          memory: 512M
    environment:
      - WORKERS=4
```

### 安全配置

```yaml
# docker-compose.security.yml
version: "3.8"
services:
  api:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    user: "1000:1000"
```

### 备份策略

```bash
#!/bin/bash
# backup.sh - 备份脚本

# 备份数据卷
docker run --rm -v langgraph-data:/data -v $(pwd):/backup alpine tar czf /backup/langgraph-data-$(date +%Y%m%d).tar.gz -C /data .

# 备份配置
cp docker-compose.yml backup/
cp .env backup/
```

## 扩展部署

### 水平扩展

```yaml
# docker-compose.scale.yml
version: "3.8"
services:
  api:
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

### 负载均衡

```yaml
# docker-compose.lb.yml
version: "3.8"
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
```

## 更多信息

- [Docker Compose 文档](https://docs.docker.com/compose/)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
- [LangGraph 部署指南](https://github.com/langchain-ai/langgraph)
