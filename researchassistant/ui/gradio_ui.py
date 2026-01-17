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

    #  on every chat this will invoke the graph with empty conversation_history, but I want to load it from memory
    conversation_history = conversation_store.get()
    

    result = graph.invoke(
        {
            "topic": user_input,
            "researched_output": "",
            "conversation_history": conversation_history['documents'],
        },
        config=config
    )

    return {
        "role": "assistant",
        "content": result["researched_output"]
    }


def refresh_facts():
    return load_all_facts()


with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Personal Research Assistant")

    with gr.Row():
        with gr.Column(scale=2):
            chat = gr.ChatInterface(
                fn=chat,  # your existing chat function
                title="Research Chat"
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
