# 使用 Python 3.11 官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY pyproject.toml ./
COPY src/ ./src/
COPY start_direct_fastapi.py ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -e .

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# 暴露端口（Railway 会自动设置 PORT 环境变量）
EXPOSE $PORT

# 健康检查（使用环境变量中的端口）
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/api/health || exit 1

# 启动命令
CMD ["python", "start_direct_fastapi.py"]
