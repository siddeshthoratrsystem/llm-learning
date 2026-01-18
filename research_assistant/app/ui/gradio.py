from dotenv import load_dotenv
load_dotenv(override=True)
from research_assistant.app.graph.edges import build_graph
import gradio as gr


config = {"configurable": {"thread_id": "user-1"}}
graph = build_graph()
session_state = {}
def chat_fn(message, history):
    state = {
        "user_input": message,
        "messages": history or []
    }
    history.append({"role": "user", "content": message})
    result = graph.invoke(state, config)
    session_state["state"] = result
    
    history.append({"role": "assistant", "content": result["final_answer"]})
    # return result["final_answer"]
    return history, result, gr.update(visible=True)

def save_note(history):
    print("Note saved!")

    state = session_state["state"]
    state["save_note_requested"] = True

    result = graph.invoke(state, config)
    print("result", result)

    session_state["state"] = result

    # Here you would add the logic to save the note to your database or storage
    return gr.update(visible=False), gr.update(visible=True)

def confirm_save_resolve_interrupt():
    state = session_state["state"]


    state["interrupt_response"] = "confirm"
    print("Confirming save...")
    result = graph.invoke(state, config=config)

    print("result after confirm", result)
    session_state["state"] = result
    return gr.update(visible=False), gr.update(visible=False)

# ui = 
with gr.Blocks() as ui:
    chatbot = gr.Chatbot()
    user_input = gr.Textbox(placeholder="Ask a question...")
    send_btn = gr.Button("Send")
    with gr.Row(visible=False) as save_section:
        text = gr.Label("Do you want to save this reply as a note?")
        save_btn = gr.Button("💾 Save note")
        skip_btn = gr.Button("Skip")

    with gr.Row(visible=False) as confirm_section:
        # show a title askign to confirm the save action
        text = gr.Label("Please confirm you want to save the note.")
        confirm_btn = gr.Button("Confirm")
        cancel_btn = gr.Button("Cancel")

    state_store = gr.State()

    send_btn.click(
        chat_fn,
        inputs=[user_input, chatbot],
        outputs=[chatbot, state_store, save_section],
    )

    skip_btn.click(
        lambda: (gr.update(visible=False), gr.update(visible=False)),
        outputs=[save_section, confirm_section],
    )

    save_btn.click(
        # lambda: (gr.update(visible=False), gr.update(visible=True)),
        # outputs=[save_section, confirm_section],
        save_note,
        inputs=[chatbot],
        outputs=[save_section, confirm_section],
    )

    confirm_btn.click(
        confirm_save_resolve_interrupt,
        inputs=[],
        outputs=[confirm_section, save_section],
    )

if __name__ == "__main__":
    ui.launch()
