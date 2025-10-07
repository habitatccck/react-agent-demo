#!/usr/bin/env python3
"""
启动直接调用 graph.invoke() 的 FastAPI 服务
无需 langgraph dev 和 langgraph_sdk
"""

import uvicorn
import os
from src.api.direct_fastapi_app import app

if __name__ == "__main__":
    # 从环境变量获取配置，Railway 会自动设置 PORT
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    reload = os.environ.get("ENVIRONMENT", "production") == "development"
    
    print("🚀 启动 LangGraph React Agent FastAPI 服务（直接调用模式）...")
    print(f"📡 服务地址: http://{host}:{port}")
    print(f"📚 API 文档: http://{host}:{port}/docs")
    print(f"💬 聊天端点: http://{host}:{port}/api/chat")
    print(f"🔧 健康检查: http://{host}:{port}/api/health")
    print("✨ 模式: 直接调用 graph.invoke()，无需 langgraph dev")
    
    if reload:
        print("🔄 开发模式：启用自动重载")
        print("按 Ctrl+C 停止服务")
    else:
        print("🚀 生产模式：优化性能")
    
    uvicorn.run(
        "src.api.direct_fastapi_app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
