from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from knowledge.medical_kb import retriever
from models.llm_model import get_llm

llm = get_llm()

# 医疗问诊提示词（合规 + 专业 + 多轮）
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    你是专业医疗问诊助手：
    1. 不做确诊，只做症状分析
    2. 主动追问：时间、发热、既往史
    3. 结合知识库给出建议
    4. 必须加免责声明
    """),
    ("user", "用户输入：{query}\n医学知识：{context}")
])

# 构建链
chain = prompt | llm | StrOutputParser()

def medical_agent(query: str) -> str:
    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])
    return chain.invoke({"query": query, "context": context})