from research_assistant.app.graph.edges import build_graph
import gradio as gr


config = {"configurable": {"thread_id": "user-1"}}
graph = build_graph()

def chat_fn(message, history):
    state = {
        "user_input": message,
        "messages": history or []
    }
    result = graph.invoke(state, config)

    return result["final_answer"]


ui = gr.ChatInterface(chat_fn)

if __name__ == "__main__":
    ui.launch()
