from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv(override=True)
class LLMClient:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )
