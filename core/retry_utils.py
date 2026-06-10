# 自动重试工具

"""
通用重试装饰器：统一配置重试策略，业务节点直接引用
"""
from tenacity import stop_after_attempt, retry, wait_exponential

from config.settings import RETRY_MAX_TIMES, RETRY_WAIT_MULTIPLIER, RETRY_WAIT_MIN, RETRY_WAIT_MAX


def auto_retry(func):
    @retry(
        stop=stop_after_attempt(RETRY_MAX_TIMES),
        wait=wait_exponential(
            multiplier=RETRY_WAIT_MULTIPLIER,
            min=RETRY_WAIT_MIN,
            max=RETRY_WAIT_MAX,
        ),
        reraise=True
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper