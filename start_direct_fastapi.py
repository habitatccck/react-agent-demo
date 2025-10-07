#!/usr/bin/env python3
"""
启动直接调用 graph.invoke() 的 FastAPI 服务
无需 langgraph dev 和 langgraph_sdk
"""

import uvicorn
from src.api.direct_fastapi_app import app

if __name__ == "__main__":
    print("🚀 启动 LangGraph React Agent FastAPI 服务（直接调用模式）...")
    print("📡 服务地址: http://localhost:8000")
    print("📚 API 文档: http://localhost:8000/docs")
    print("💬 聊天端点: http://localhost:8000/api/chat")
    print("🔧 健康检查: http://localhost:8000/api/health")
    print("✨ 模式: 直接调用 graph.invoke()，无需 langgraph dev")
    print("按 Ctrl+C 停止服务")
    
    uvicorn.run(
        "src.api.direct_fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式下自动重载
        log_level="info"
    )
