from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from models.llm_model import get_embedding
from config.settings import VECTOR_DIR

# 这里是模拟的数据，可替换成真实的pdf
MEDICAL_KNOWLEDGE = """
1. 咳嗽>3天+黄痰+胸闷 → 支气管炎 → 呼吸科
2. 头痛+发热+鼻塞 → 上呼吸道感染 → 全科
3. 胃痛反酸 → 胃炎 → 消化科
4. 皮肤红疹瘙痒 → 过敏性皮炎 → 皮肤科
5. 心慌胸闷 → 心内科
6. 关节肿痛 → 骨科/风湿科
7. 腹痛腹泻 → 消化内科
"""

def build_knowledge():
    splitter = RecursiveCharacterTextSplitter()
    chunks = splitter.split_text(MEDICAL_KNOWLEDGE)
    embedding = get_embedding()
    db = Chroma.from_texts(chunks, embedding, persist_directory=VECTOR_DIR)
    return db.as_retriever(search_kwargs={"k": 2})

# 加载检索器
retriever = build_knowledge()