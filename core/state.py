# TypedDict 状态定义

"""
LangGraph 全局状态定义
使用 TypedDict 做强类型约束，规范多节点间数据流转
"""
import operator
from typing import TypedDict, Annotated


class AgentState(TypedDict):
    user_query: str  # 用户原始提问
    department: str  # 分诊结果-科室
    messages: Annotated[list, operator.add]  # 对话消息列表
    answer: str  # 最终回答内容
    error: str  # 异常信息
