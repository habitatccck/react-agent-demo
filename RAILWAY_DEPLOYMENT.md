# Railway 部署指南

## 概述

本指南将帮助您在 Railway 云平台上部署 LangGraph React Agent 服务，并通过公网 IP 访问。

## 部署步骤

### 1. 准备环境变量

在 Railway 控制台中设置以下环境变量：

#### 必需的环境变量：

- `OPENAI_API_KEY`: 你的 OpenAI API 密钥
- `TAVILY_API_KEY`: Tavily 搜索 API 密钥（用于搜索功能）

#### 可选的环境变量：

- `OPENAI_BASE_URL`: OpenAI API 基础 URL（如果使用代理）
- `MODEL_NAME`: 模型名称（默认：openai/gpt-4o-mini）
- `MAX_SEARCH_RESULTS`: 最大搜索结果数（默认：10）
- `ENVIRONMENT`: 环境类型（production/development）

### 2. 部署到 Railway

#### 方法一：通过 Railway CLI

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录 Railway
railway login

# 初始化项目
railway init

# 部署
railway up
```

#### 方法二：通过 GitHub 集成

1. 将代码推送到 GitHub 仓库
2. 在 Railway 控制台连接 GitHub 仓库
3. Railway 会自动检测 Dockerfile 并部署

### 3. 配置说明

#### 端口配置

- Railway 会自动设置 `PORT` 环境变量
- 服务会自动绑定到 `0.0.0.0:PORT`
- 无需手动配置端口映射

#### 健康检查

- 健康检查端点：`/api/health`
- Railway 会自动监控服务状态

### 4. 访问服务

部署成功后，Railway 会提供一个公网 URL，格式类似：

```
https://your-app-name.railway.app
```

#### 主要端点：

- **根路径**: `https://your-app-name.railway.app/`
- **API 文档**: `https://your-app-name.railway.app/docs`
- **聊天端点**: `https://your-app-name.railway.app/api/chat`
- **健康检查**: `https://your-app-name.railway.app/api/health`

### 5. 测试部署

#### 健康检查

```bash
curl https://your-app-name.railway.app/api/health
```

#### 聊天测试

```bash
curl -X POST https://your-app-name.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，请介绍一下你自己",
    "conversation_id": "test-001"
  }'
```

### 6. 监控和日志

- 在 Railway 控制台查看实时日志
- 监控服务状态和性能指标
- 设置自动重启策略

### 7. 故障排除

#### 常见问题：

1. **服务启动失败**

   - 检查环境变量是否正确设置
   - 查看 Railway 日志获取详细错误信息

2. **API 调用失败**

   - 确认 OpenAI API 密钥有效
   - 检查网络连接和防火墙设置

3. **端口绑定错误**
   - Railway 会自动处理端口配置
   - 确保使用 `PORT` 环境变量

### 8. 性能优化

- 设置 `ENVIRONMENT=production` 禁用开发模式
- 配置适当的资源限制
- 启用健康检查和自动重启

## 注意事项

1. **安全性**：确保 API 密钥安全存储，不要在代码中硬编码
2. **资源限制**：Railway 有资源使用限制，注意监控使用情况
3. **域名**：Railway 提供免费域名，也可以绑定自定义域名
4. **备份**：定期备份重要数据和配置

## 支持

如果遇到问题，请检查：

1. Railway 控制台的日志输出
2. 环境变量配置
3. 网络连接状态
4. API 密钥有效性
