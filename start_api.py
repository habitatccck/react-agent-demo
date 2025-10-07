#!/usr/bin/env python3
"""启动HTTP API服务

这个脚本用于启动LangGraph HTTP API服务。
"""

import os
import sys
import uvicorn
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def main():
    """启动HTTP API服务"""
    
    # 设置环境变量
    os.environ.setdefault("API_HOST", "0.0.0.0")
    os.environ.setdefault("API_PORT", "8000")
    os.environ.setdefault("LANGGRAPH_API_URL", "http://localhost:2024")
    
    # 获取配置
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    langgraph_url = os.getenv("LANGGRAPH_API_URL", "http://localhost:2024")
    
    print("🚀 启动 LangGraph HTTP API 服务")
    print("=" * 50)
    print(f"🌐 服务地址: http://{host}:{port}")
    print(f"📚 API文档: http://{host}:{port}/docs")
    print(f"📡 LangGraph服务器: {langgraph_url}")
    print("=" * 50)
    print("💡 使用说明:")
    print("  - POST /api/chat - 聊天接口")
    print("  - GET /api/threads - 获取线程列表")
    print("  - GET /health - 健康检查")
    print("  - GET /docs - API文档")
    print("=" * 50)
    
    # 启动服务
    uvicorn.run(
        "api.http_service:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
