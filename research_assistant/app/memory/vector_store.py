from datetime import datetime
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

db = Chroma(
    collection_name="notes",
    embedding_function=OpenAIEmbeddings()
)

def save_note(note: str):
    db.add_texts([note])

conversations = Chroma(
    collection_name="conversations",
    embedding_function=OpenAIEmbeddings()
)

def save_conversation(user_input, assistant_reply, thread_id):
    doc_text = f"""
    User:
    {user_input}

    Assistant:
    {assistant_reply}
    """.strip()

    conversations.add_texts(
        texts=[doc_text],
        metadatas=[{
            "type": "conversation",
            "thread_id": thread_id,
            "timestamp": datetime.utcnow().isoformat()
        }]
    )