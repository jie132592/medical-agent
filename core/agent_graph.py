# LangGraph 工作流 + 节点逻辑
"""
LangGraph 多智能体工作流核心
规则：节点内部使用 create_agent，挂载中间件、重试、降级
"""
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.llms import Ollama
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt.tool_node import tools_condition

# 内部模块导入
from config.settings import TEMPERATURE, DEGRADE_TIP, LLM_MODEL_NAME
from core.middleware import MedicalAgentMiddleware
from core.retry_utils import auto_retry
from core.state import AgentState
from tools.medical_tools import triage_tool, medical_rag_tool


class MedicalAgentGraph:
    def __init__(self):
        # 初始化大模型
        self.llm = Ollama(
            model=LLM_MODEL_NAME,
            temperature=TEMPERATURE,
            base_url="http://localhost:11434"
        )

        # 初始化中间件、工具
        self.tools = [triage_tool, medical_rag_tool]
        self.middleware = MedicalAgentMiddleware()  # 修复拼写错误
        self.tool_node = ToolNode(self.tools)

        # 定义Agent提示词
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是专业医疗助手，必须调用工具回答，禁止编造。"),
            ("placeholder", "{messages}"),
        ])

        # 构建工作流
        self.workflow = StateGraph(AgentState)
        self._build_graph()
        self.app = self.workflow.compile()

        # ====================== 修复：生成 Mermaid 流程图 ======================
        print("\n" + "=" * 50)
        print("📊 工作流 Mermaid 流程图：")
        print("=" * 50)
        print(self.app.get_graph().draw_mermaid())
        print("=" * 50 + "\n")

    def triage_node(self, state: AgentState) -> dict:
        """分诊节点：独立节点，完成科室判断"""
        dept = triage_tool.invoke(state["user_query"])
        return {"department": dept}

    @auto_retry
    def agent_decision_node(self, state: AgentState) -> dict:
        """核心决策节点 规则：节点内部创建 create_agent + 挂载中间件"""
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({"messages": state["messages"]})

            # ✅ 绝对安全：只更新 answer，不碰 messages！
            return {"answer": response}

        except Exception as e:
            err_msg = f"{DEGRADE_TIP}\n异常：{str(e)}"
            return {"answer": err_msg}

    def _build_graph(self):
        """编排节点与连接"""
        # 节点注册
        self.workflow.add_node("triage", self.triage_node)
        self.workflow.add_node("agent", self.agent_decision_node)
        self.workflow.add_node("tools", self.tool_node)

        self.workflow.add_edge(START, "triage")
        self.workflow.add_edge("triage", "agent")
        self.workflow.add_edge("agent", END)

    def run(self, user_input: str) -> str:
        """对外调用入口"""
        init_state = {
            "user_query": user_input,
            "department": "",
            "messages": [HumanMessage(content=user_input)],
            "answer": "",
            "error": ""
        }
        res = self.app.invoke(init_state)
        answer = res["answer"]
        return f"【建议科室】{res['department']}\n\n{answer}"