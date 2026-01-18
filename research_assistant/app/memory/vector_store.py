from datetime import datetime
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

db = Chroma(
    collection_name="notes",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)

def save_note(note: str):
    db.add_texts([note])

conversations = Chroma(
    collection_name="conversations",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)

def save_conversation(user_input, assistant_reply, thread_id):
    doc_text = f"""
    User:
    {user_input}

    Assistant:
    {assistant_reply}
    """.strip()

    print("inside save_conversation, thread_id=", thread_id, user_input, assistant_reply)
    conversations.add_texts(
        texts=[doc_text],
        metadatas=[{
            "type": "conversation",
            "thread_id": thread_id,
            "timestamp": datetime.utcnow().isoformat()
        }]
    )

def load_notes():
    results = db.get()

    rows = []
    print("results", results)
    for i, doc in enumerate(results["documents"]):
        rows.append(doc)

    print("notes testing", rows)
    return rows

def load_conversations():
    where = {"type": "conversation"}
    results = conversations.get()

    rows = []

    for i, doc_text in enumerate(results["documents"]):
        metadata = results["metadatas"][i]

        user_msg = ""
        assistant_msg = ""

        if "User:" in doc_text and "Assistant:" in doc_text:
            user_part, assistant_part = doc_text.split("Assistant:", 1)
            user_msg = user_part.replace("User:", "").strip()
            assistant_msg = assistant_part.strip()


        rows.append([
            metadata.get("timestamp"),
            user_msg,
            assistant_msg,
        ])

    return rows

