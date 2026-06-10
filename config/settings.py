"""
全局配置文件：模型、限流、重试阈值、系统文案统一管理
"""
LLM_MODEL_NAME = 'deepseek-r1:1.5b'
TEMPERATURE = 0.1

# 限流配置
MAX_MODEL_CALL_LIMIT = 15

# 重试配置
RETRY_MAX_TIMES = 3
RETRY_WAIT_MULTIPLIER = 1
RETRY_WAIT_MIN = 1
RETRY_WAIT_MAX = 5

# 降级提升文案
DEGRADE_TIP = "服务降级：系统繁忙，请前往医院全科就诊"