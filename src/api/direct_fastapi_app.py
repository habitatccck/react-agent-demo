"""
直接调用 graph.invoke() 的 FastAPI 服务
不依赖 langgraph dev 和 langgraph_sdk
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
import json
import os
from dotenv import load_dotenv

# 导入我们的图和相关组件
from react_agent.graph import graph
from react_agent.context import Context
from react_agent.state import InputState
from langchain_core.messages import HumanMessage, AIMessage

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="LangGraph React Agent API (Direct)",
    description="直接调用 LangGraph React Agent 大模型能力，无需 langgraph dev",
    version="1.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"
    model: str = "openai/gpt-4o-mini"  # 可选：指定模型
    max_search_results: int = 10  # 可选：指定搜索结果数量

# 响应模型
class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    status: str = "success"
    model_used: str

# 存储对话历史的简单字典（生产环境建议使用数据库）
conversation_history: Dict[str, List[Dict[str, str]]] = {}

@app.get("/")
async def root():
    return {
        "message": "LangGraph React Agent API 服务正在运行（直接调用模式）", 
        "endpoints": ["/api/chat"],
        "mode": "direct_graph_invoke"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天端点，直接调用 graph.invoke() 而不使用 langgraph dev
    """
    try:
        # 获取或初始化对话历史
        if request.conversation_id not in conversation_history:
            conversation_history[request.conversation_id] = []
        
        # 添加用户消息到历史
        conversation_history[request.conversation_id].append({
            "role": "human",
            "content": request.message
        })
        
        # 准备输入数据 - 转换为 LangChain 消息格式
        messages = []
        for msg in conversation_history[request.conversation_id]:
            if msg["role"] == "human":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # 创建上下文配置
        context = Context(
            model=request.model,
            max_search_results=request.max_search_results
        )
        
        # 准备输入状态
        input_state = InputState(messages=messages)
        
        # 直接调用图
        ai_response = ""
        try:
            # 使用 graph.ainvoke() 直接调用，使用 context 参数
            result = await graph.ainvoke(
                input_state,
                context=context
            )
            
            # 从结果中提取 AI 响应
            if "messages" in result and result["messages"]:
                # 获取最后一条 AI 消息
                for message in reversed(result["messages"]):
                    if isinstance(message, AIMessage) and not message.tool_calls:
                        ai_response = message.content
                        break
                    elif hasattr(message, 'type') and message.type == 'ai':
                        ai_response = getattr(message, 'content', '')
                        break
                    elif isinstance(message, dict) and message.get('type') == 'ai':
                        ai_response = message.get('content', '')
                        break
            
        except Exception as e:
            print(f"Graph 调用出错: {e}")
            ai_response = f"调用图时出错: {str(e)}"
        
        # 如果没有获取到响应，使用默认消息
        if not ai_response:
            ai_response = "抱歉，我无法处理您的请求。"
        
        # 添加 AI 响应到历史
        conversation_history[request.conversation_id].append({
            "role": "assistant", 
            "content": ai_response
        })
        
        return ChatResponse(
            response=ai_response,
            conversation_id=request.conversation_id,
            status="success",
            model_used=request.model
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

@app.get("/api/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    """
    获取指定对话的历史记录
    """
    if conversation_id not in conversation_history:
        return {"messages": [], "conversation_id": conversation_id}
    
    return {
        "messages": conversation_history[conversation_id],
        "conversation_id": conversation_id
    }

@app.delete("/api/chat/history/{conversation_id}")
async def clear_chat_history(conversation_id: str):
    """
    清除指定对话的历史记录
    """
    if conversation_id in conversation_history:
        del conversation_history[conversation_id]
        return {"message": f"对话 {conversation_id} 的历史记录已清除"}
    else:
        return {"message": f"对话 {conversation_id} 不存在"}

@app.get("/api/health")
async def health_check():
    """
    健康检查端点
    """
    return {
        "status": "healthy",
        "mode": "direct_graph_invoke",
        "graph_available": graph is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
