from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

db = Chroma(
    collection_name="notes",
    embedding_function=OpenAIEmbeddings()
)

def save_note(note: str):
    db.add_texts([note])
