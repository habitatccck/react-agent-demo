#!/bin/bash

# 简洁的 Docker 运行脚本

echo "🐳 启动 React Agent FastAPI 服务..."

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "📝 创建 .env 文件..."
    cp env.example .env
    echo "⚠️  请编辑 .env 文件，设置正确的 API 密钥"
    exit 1
fi

# 创建日志目录
mkdir -p logs

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d --build

echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    echo "📡 API 地址: http://localhost:8000"
    echo "📚 API 文档: http://localhost:8000/docs"
    echo ""
    echo "📋 常用命令："
    echo "  查看日志: docker-compose logs -f"
    echo "  停止服务: docker-compose down"
else
    echo "❌ 服务启动失败，查看日志："
    docker-compose logs
fi
