# AgentMiddleware 限流/请求拦截
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse, ExtendedModelResponse

from config.settings import MAX_MODEL_CALL_LIMIT

"""
自定义代理中间件
继承官方 AgentMiddleware，实现模型调用限流、请求/响应拦截
"""


class MedicalAgentMiddleware(AgentMiddleware):
    def __init__(self):
        self.call_count = 0
        self.max_calls = MAX_MODEL_CALL_LIMIT

    def on_model_request(self, request: ModelRequest) -> ModelRequest:
        """模型发起请求前：计数 + 限流熔断"""
        self.call_count += 1
        if self.call_count > self.max_calls:
            raise Exception("模型调用次数超出上限，触发限流")
        return request

    def on_model_response(self, request: ModelRequest, response: ModelResponse) -> ExtendedModelResponse:
        """模型返回响应后：扩展元数据、日志埋点"""
        return ExtendedModelResponse(
            content=response.content,
            metadata={"middleware_flag": "processed", "module": "medical_agent"}
        )