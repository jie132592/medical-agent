import gradio as gr
from core.multi_agent import medical_team_chat
from utils.prompt_utils import add_disclaimer

def chat(message, history):
    response = medical_team_chat(message)
    return add_disclaimer(response)

# 网页界面
# 网页界面
with gr.Blocks(title="医疗Agent") as demo:
    gr.Markdown("# 🏥 模块化医疗问诊 Agent (简历项目)")
    gr.Markdown("## 功能：多智能体分诊 + RAG知识库 + 合规问诊")
    gr.ChatInterface(chat)

if __name__ == '__main__':
    demo.launch(server_port=7860)