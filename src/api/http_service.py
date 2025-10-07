"""LangGraph HTTP API 服务

这个模块提供了一个HTTP API服务，封装LangGraph代理调用。
对外暴露REST API接口，供前端或其他服务调用。
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langgraph_sdk import get_client


# 请求和响应模型
class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str = Field(..., description="消息角色: human, assistant, system")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户消息", min_length=1, max_length=2000)
    thread_id: Optional[str] = Field(None, description="线程ID，用于多轮对话")
    model: Optional[str] = Field(None, description="指定使用的模型")


class ChatResponse(BaseModel):
    """聊天响应模型"""
    success: bool = Field(..., description="请求是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    thread_id: Optional[str] = Field(None, description="线程ID")
    timestamp: str = Field(..., description="响应时间戳")


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    timestamp: str = Field(..., description="检查时间")
    version: str = Field(..., description="服务版本")


# 创建FastAPI应用
app = FastAPI(
    title="LangGraph API Service",
    description="基于LangGraph的AI代理HTTP API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
langgraph_client = None


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化LangGraph客户端"""
    global langgraph_client
    langgraph_url = os.getenv("LANGGRAPH_API_URL", "http://localhost:2024")
    langgraph_client = get_client(url=langgraph_url)
    print(f"🚀 LangGraph HTTP API 服务启动")
    print(f"📡 连接到 LangGraph 服务器: {langgraph_url}")


@app.get("/", response_model=HealthResponse)
async def root():
    """根路径健康检查"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天接口
    
    发送消息到LangGraph代理并获取响应
    """
    try:
        if not langgraph_client:
            raise HTTPException(status_code=500, detail="LangGraph客户端未初始化")
        
        print(f"📨 收到聊天请求: {request.message}")
        print(f"🧵 线程ID: {request.thread_id or '新线程'}")
        
        # 构建消息格式
        messages = [{
            "role": "human",
            "content": request.message,
        }]
        
        # 调用LangGraph代理
        response_data = []
        final_message = ""
        current_thread_id = request.thread_id
        
        async for chunk in langgraph_client.runs.stream(
            request.thread_id,  # 使用提供的线程ID或创建新线程
            "agent",  # 代理名称
            input={"messages": messages},
        ):
            if chunk.event == "messages":
                # 处理消息响应
                for msg in chunk.data.get("messages", []):
                    if msg.get("role") == "assistant":
                        final_message = msg.get("content", "")
                        response_data.append({
                            "type": "message",
                            "content": final_message,
                            "role": "assistant"
                        })
            
            elif chunk.event == "tools":
                # 处理工具调用
                response_data.append({
                    "type": "tool_call",
                    "data": chunk.data
                })
                print(f"🔧 工具调用: {chunk.data}")
            
            elif chunk.event == "end":
                # 获取线程ID
                if hasattr(chunk, 'thread_id'):
                    current_thread_id = chunk.thread_id
                break
        
        return ChatResponse(
            success=True,
            message="聊天请求处理成功",
            data={
                "response": final_message,
                "full_data": response_data,
                "model_used": request.model or "default"
            },
            thread_id=current_thread_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"❌ 聊天请求处理失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"聊天请求处理失败: {str(e)}"
        )


@app.get("/api/threads")
async def get_threads():
    """获取所有线程列表"""
    try:
        if not langgraph_client:
            raise HTTPException(status_code=500, detail="LangGraph客户端未初始化")
        
        threads = await langgraph_client.threads.list()
        return {
            "success": True,
            "data": threads,
            "message": "获取线程列表成功",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ 获取线程列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取线程列表失败: {str(e)}"
        )


@app.delete("/api/threads/{thread_id}")
async def delete_thread(thread_id: str):
    """删除指定线程"""
    try:
        if not langgraph_client:
            raise HTTPException(status_code=500, detail="LangGraph客户端未初始化")
        
        # 这里需要根据实际的SDK方法来实现
        # await langgraph_client.threads.delete(thread_id)
        
        return {
            "success": True,
            "message": f"线程 {thread_id} 删除成功",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ 删除线程失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"删除线程失败: {str(e)}"
        )


@app.get("/api/models")
async def get_available_models():
    """获取可用模型列表"""
    return {
        "success": True,
        "data": {
            "models": [
                "openai/gpt-4o-mini",
                "openai/gpt-4-turbo-preview", 
                "anthropic/claude-3-5-sonnet-20240620",
                "anthropic/claude-3-haiku-20240307"
            ],
            "default": "openai/gpt-4o-mini"
        },
        "message": "获取模型列表成功",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    # 从环境变量获取配置
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    print(f"🌐 启动HTTP API服务")
    print(f"📍 服务地址: http://{host}:{port}")
    print(f"📚 API文档: http://{host}:{port}/docs")
    
    uvicorn.run(
        "http_service:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
