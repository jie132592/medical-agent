from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from config.settings import LLM_MODEL, TEMPERATURE, EMBEDDING_MODEL
import os
load_dotenv()


def get_llm():
    return Ollama(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434",
    temperature=0.7
)


def get_embedding():
    return OllamaEmbeddings(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434"
)
