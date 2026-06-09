# 多智能体：分诊Agent + 问诊Agent
from core.medical_agent import medical_agent

def triage_agent(symptom: str):
    if "咳嗽" in symptom or "胸闷" in symptom:
        return "呼吸科"
    elif "胃痛" in symptom or "反酸" in symptom:
        return "消化科"
    elif "皮肤" in symptom or "痒" in symptom:
        return "皮肤科"
    elif "头痛" in symptom or "发烧" in symptom:
        return "全科"
    elif "心慌" in symptom:
        return "心内科"
    else:
        return "全科"

# 团队协作
def medical_team_chat(query: str):
    # 1. 分诊
    department = triage_agent(query)
    # 问诊
    answer = medical_agent(query)
    # 最终回复
    return f"【建议科室】{department}\n\n{answer}"