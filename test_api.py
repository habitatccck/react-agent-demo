#!/usr/bin/env python3
"""测试HTTP API服务

这个脚本用于测试LangGraph HTTP API服务。
"""

import requests
import json
import time

# API服务地址
API_BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_chat(message: str, thread_id: str = None):
    """测试聊天接口"""
    print(f"💬 测试聊天: {message}")
    
    payload = {
        "message": message,
    }
    
    if thread_id:
        payload["thread_id"] = thread_id
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 聊天成功")
            print(f"🤖 AI回复: {data['data']['response']}")
            print(f"🧵 线程ID: {data['thread_id']}")
            return data['thread_id']
        else:
            print(f"❌ 聊天失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 聊天请求失败: {e}")
        return None

def test_threads():
    """测试获取线程列表"""
    print("📋 测试获取线程列表...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/threads")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 获取线程列表失败: {e}")
        return False

def test_models():
    """测试获取模型列表"""
    print("🤖 测试获取模型列表...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/models")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 获取模型列表失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试 LangGraph HTTP API 服务")
    print("=" * 60)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(2)
    
    # 测试健康检查
    if not test_health():
        print("❌ 服务未启动，请先启动API服务")
        return
    
    print("\n" + "=" * 60)
    
    # 测试获取模型列表
    test_models()
    
    print("\n" + "=" * 60)
    
    # 测试聊天
    thread_id = test_chat("你好，请介绍一下你自己")
    
    if thread_id:
        print("\n" + "=" * 60)
        # 测试多轮对话
        test_chat("请搜索最新的AI技术发展", thread_id)
    
    print("\n" + "=" * 60)
    
    # 测试获取线程列表
    test_threads()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")

if __name__ == "__main__":
    main()
