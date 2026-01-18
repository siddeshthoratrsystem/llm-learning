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
        "messages": history or [],
        "thread_id": config["configurable"]["thread_id"],
    }
    # history.append({"role": "user", "content": message})

    # Show user immediately
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": ""})
    yield history, None, gr.update(visible=False)

    # result = graph.invoke(state, config)
    # session_state["state"] = result
    
    # history.append({"role": "assistant", "content": result["final_answer"]})
    assistant_text = ""

    count = 0
    for event in graph.stream(state, config):
        print("Event:", event, count)
        count += 1
        if "save_note_handler" in event:
            save_note_handler = event["save_note_handler"]
            if "final_answer" in save_note_handler:
                assistant_text += save_note_handler["final_answer"]
                history[-1]["content"] = assistant_text
                # print("Inside the loop Final assistant text:", assistant_text)
                yield history, None, gr.update(visible=False)
    # return result["final_answer"]
    
    print("Final assistant text:", history)
    # history[-1]["content"] = session_state.get("state", {}).get("final_answer", assistant_text)
    session_state["state"] = {
        **state,
        "final_answer": assistant_text,
    }

    yield history, session_state["state"], gr.update(visible=True)

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

def cancel_save_resolve_interrupt():
    state = session_state["state"]


    state["interrupt_response"] = "cancel"
    print("Cancelling...")
    result = graph.invoke(state, config=config)

    print("result after cancelling", result)
    session_state["state"] = result
    return gr.update(visible=False), gr.update(visible=False)

# ui = 
with gr.Blocks(css="""
    #chatbot {height: 500px}
    #input-row {position: sticky; bottom: 0;}
    """) as ui:


    chatbot = gr.Chatbot(elem_id="chatbot")

    with gr.Row(elem_id="input-row"):
        user_input = gr.Textbox(
            placeholder="Ask a question...",
            scale=8,
            container=False
        )
        send_btn = gr.Button("Send", scale=1)

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
    cancel_btn.click(
        cancel_save_resolve_interrupt,
        inputs=[],
        outputs=[confirm_section, save_section],
    )

if __name__ == "__main__":
    ui.launch()
