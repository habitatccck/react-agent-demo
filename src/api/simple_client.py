"""简单的 LangGraph API 客户端示例

这是一个简化的API调用示例，适合快速测试。
"""

import asyncio
from langgraph_sdk import get_client


async def simple_chat(message: str):
    """简单的聊天函数
    
    Args:
        message: 要发送的消息
    """
    # 创建客户端
    client = get_client(url="http://localhost:2024")
    
    print(f"🤖 发送消息: {message}")
    print("⏳ 等待响应...")
    print("-" * 50)
    
    try:
        async for chunk in client.runs.stream(
            None,  # 创建新线程
            "agent",  # 代理名称
            input={
                "messages": [{
                    "role": "human",
                    "content": message,
                }],
            },
        ):
            if chunk.event == "messages":
                # 打印AI的响应
                for msg in chunk.data.get("messages", []):
                    if msg.get("role") == "assistant":
                        print(f"🤖 AI回复: {msg.get('content', '')}")
            
            elif chunk.event == "tools":
                # 打印工具调用信息
                print(f"🔧 使用工具: {chunk.data}")
            
            elif chunk.event == "end":
                print("✅ 对话结束")
                break
                
    except Exception as e:
        print(f"❌ 错误: {e}")


async def main():
    """主函数"""
    print("🚀 LangGraph API 客户端启动")
    print("=" * 50)
    
    # 测试对话
    await simple_chat("你好，请介绍一下你自己")
    
    print("\n" + "=" * 50)
    await simple_chat("请搜索最新的Python编程趋势")


if __name__ == "__main__":
    asyncio.run(main())
