from dotenv import load_dotenv
load_dotenv()

from researchassistant.memory.chroma import conversation_store
import os
from researchassistant.graph import graph
import gradio as gr
from researchassistant.memory.utils import load_all_facts

# Later create a separate file for this
import gradio as gr
# =========================================================
# GRADIO UI
# =========================================================
config = {"configurable": {"thread_id": "user-1"}}
def chat(user_input, history):

    print("User input:", user_input)


    conversation_store.add_texts(
        ["USER: " + user_input],
        metadatas=[{"conversation_id": "conv_user-1"}]
    )

    result = graph.invoke(
        {
            "topic": user_input,
            "researched_output": "",
            "conversation_history": history or [],
            "conversation_id": "conv_user-1"
        },
        config=config
    )

    conversation_store.add_texts(
        ["MODAL: " + result['researched_output']],
        metadatas=[{"conversation_id": "conv_user-1"}]
    )


    all_con = conversation_store._collection.get().get("documents", [])
    print("All conversation stored:", all_con)
    # append conversation in state and in a DB based on conversation_id

    return {
        "role": "assistant",
        "content": result["researched_output"]
    }


def refresh_facts():
    return load_all_facts()

def load_conversation_for_ui():
    results = conversation_store._collection.get(
        where={"conversation_id": "conv_user-1"},
        limit=100
    )

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    chat_messages = []

    print("Loaded conversation:", documents, metadatas)
    for text, meta in zip(documents, metadatas):
        role = "user" if text.startswith("USER: ") else "assistant"
        text = text.replace("USER: ", "").replace("MODAL: ", "")
        chat_messages.append({
            "role": role,
            "content": text
        })


    return chat_messages


with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Personal Research Assistant")

    with gr.Row():
        with gr.Column(scale=2):
            chat = gr.ChatInterface(
                fn=chat,  # your existing chat function
                title="Research Chat",
                chatbot=gr.Chatbot(value=load_conversation_for_ui())
            )

        with gr.Column(scale=1):
            gr.Markdown("### 📚 Stored Facts")

            facts_table = gr.Dataframe(
                headers=["fact"],
                datatype=["str"],
                interactive=False
            )

            refresh_btn = gr.Button("🔄 Refresh Facts")

            refresh_btn.click(
                refresh_facts,
                outputs=facts_table
            )

    # Load facts on startup
    demo.load(
        refresh_facts,
        outputs=facts_table
    )

demo.launch()
