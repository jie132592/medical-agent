from langchain_core.tools import tool
"""
医疗业务工具：分诊工具 + 知识库检索工具
解耦工具与工作流，便于后续扩展新工具
"""

@tool
def triage_tool(symptom: str) -> str:
    """
    分诊工具：根据用户症状推荐就诊科室
    Args:
        symptom：用户描述的症状
    Returns:
         推荐科室名称
    """
    symptom = symptom.lower()
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
    return "全科"

@tool
def medical_rag_tool(query: str) -> str:
    """
    医学知识库检索工具：返回标准医学参考知识
    Args:
        query: 用户问题/症状
    Returns:
        知识库文本
    """
    return """
    咳嗽、胸闷 → 支气管炎 → 呼吸科
    胃痛、反酸 → 胃炎/反流性食管炎 → 消化科
    皮肤红疹、瘙痒 → 过敏性皮炎 → 皮肤科
    头痛、发烧、鼻塞 → 上呼吸道感染 → 全科
    心慌、心悸 → 需排查心脏问题 → 心内科
    """