"""定义一个自定义的推理和行动代理。

支持工具调用的聊天模型。
"""

from datetime import UTC, datetime
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.runtime import Runtime

from react_agent.context import Context
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model

# 定义调用模型的函数


async def call_model(
    state: State, 
    runtime: Runtime[Context]
) -> Dict[str, List[AIMessage]]:
    """调用驱动我们"代理"的大语言模型。

    此函数准备提示词，初始化模型，并处理响应。

    Args:
        state (State): 对话的当前状态。
        config (RunnableConfig): 模型运行的配置。

    Returns:
        dict: 包含模型响应消息的字典。
    """
    # 初始化带有工具绑定的模型。在此处更改模型或添加更多工具。
    model = load_chat_model(runtime.context.model).bind_tools(TOOLS)

    # 格式化系统提示词。自定义此部分以更改代理的行为。
    system_message = runtime.context.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )

    # 获取模型的响应
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages]
        ),
    )

    # 处理最后一步时模型仍想使用工具的情况
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="抱歉，我在指定的步骤数内无法找到您问题的答案。",
                )
            ]
        }

    # 将模型的响应作为列表返回，添加到现有消息中
    return {"messages": [response]}


# 定义一个新的图

builder = StateGraph(State, input_schema=InputState, context_schema=Context)

# 定义我们将在其间循环的两个节点
builder.add_node(call_model)
builder.add_node("tools", ToolNode(TOOLS))

# 将入口点设置为 `call_model`
# 这意味着此节点是第一个被调用的
builder.add_edge("__start__", "call_model")


def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """根据模型的输出确定下一个节点。

    此函数检查模型的最后一条消息是否包含工具调用。

    Args:
        state (State): 对话的当前状态。

    Returns:
        str: 要调用的下一个节点的名称（"__end__" 或 "tools"）。
    """
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )
    # 如果没有工具调用，则结束
    if not last_message.tool_calls:
        return "__end__"
    # 否则执行请求的操作
    return "tools"


# 添加条件边以确定 `call_model` 之后的下一步
builder.add_conditional_edges(
    "call_model",
    # call_model 运行完成后，下一个节点将根据
    # route_model_output 的输出进行调度
    route_model_output,
)

# 从 `tools` 到 `call_model` 添加普通边
# 这创建了一个循环：使用工具后，我们总是返回到模型
builder.add_edge("tools", "call_model")

# 将构建器编译为可执行图
graph = builder.compile(name="ReAct Agent")
