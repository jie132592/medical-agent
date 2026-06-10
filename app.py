import gradio as gr
from core.agent_graph import MedicalAgentGraph

# 初始化全局智能体工作流
agent_app = MedicalAgentGraph()

def chat_handler(message: str, history) -> str:
    """聊天交互"""
    return agent_app.run(message)

if __name__ == '__main__':
    # 启动Gradio界面
    with gr.Blocks(title="企业级医疗多智能体系统") as demo:
        gr.Markdown("# 🏥 医疗问诊多智能体 | LangGraph + AgentMiddleware")
        gr.ChatInterface(chat_handler)

    demo.launch(server_port=7860, server_name="127.0.0.1")