# 🏥 医疗问诊智能体（模块化企业级项目）
基于 LLM + RAG + 多智能体的医疗问诊分诊系统，可进行症状咨询、智能分诊、医学知识库检索。

## 项目亮点
- 模块化工程架构（config/core/knowledge/models/utils）
- 多智能体协作：分诊Agent + 问诊Agent
- RAG 医学知识库，降低模型幻觉
- 医疗合规输出，带免责声明
- Gradio 可视化界面，可直接演示

## 技术栈
Python、LangChain、LangGraph、Chroma、RAG、Gradio、LLM

## 运行方式
```bash
pip install -r requirements.txt
python app.py
