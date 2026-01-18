from dotenv import load_dotenv
load_dotenv(override=True)

from research_assistant.app.memory.vector_store import load_conversations
from research_assistant.app.memory.vector_store import load_notes

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
    yield history, None, gr.update(visible=False), load_conversations()

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
                yield history, None, gr.update(visible=False), load_conversations(),
    # return result["final_answer"]
    
    print("Final assistant text:", history)
    # history[-1]["content"] = session_state.get("state", {}).get("final_answer", assistant_text)
    session_state["state"] = {
        **state,
        "final_answer": assistant_text,
    }

    yield history, session_state["state"], gr.update(visible=True), load_conversations()

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
    return gr.update(visible=False), gr.update(visible=False), load_notes()

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
    .action-card {
        padding: 12px 14px;
        border-radius: 10px;
        background: #f6f7f9;
        margin-bottom: 8px;
        color: #666;
    }

    .title {
        color: black;
        font-size: 15px;
    }

    .action-card.warning {
        background: #fff4e5;
    }

    .action-subtext {
        font-size: 15px;
        color: #666;
        margin-top: 4px;
    }

    """) as ui:


    chatbot = gr.Chatbot(elem_id="chatbot")

    with gr.Row(elem_id="input-row"):
        user_input = gr.Textbox(
            placeholder="Ask a question...",
            scale=8,
            container=False
        )
        send_btn = gr.Button("Send", scale=1)

    with gr.Column(visible=False, elem_id="save_section") as save_section:
        gr.Markdown(
            """
            <div class="action-card">
                <b class="title">Save this reply as a note?</b>
                <div class="action-subtext">
                    You can access it later from Notes.
                </div>
            </div>
            """
        )

        with gr.Row():
            save_btn = gr.Button("💾 Save", variant="primary")
            skip_btn = gr.Button("Skip", variant="secondary")


    with gr.Column(visible=False, elem_id="confirm_section") as confirm_section:
        gr.Markdown(
            """
            <div class="action-card warning">
                <b class="title">Confirm save</b>
                <div class="action-subtext">
                    This action cannot be undone.
                </div>
            </div>
            """
        )

        with gr.Row():
            confirm_btn = gr.Button("Confirm", variant="primary")
            cancel_btn = gr.Button("Cancel", variant="secondary")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Saved Notes")
            notes_table = gr.Dataframe(
                headers=["SavedNotes"],
                datatype=["str"],
                interactive=False
            )

        with gr.Column(scale=1):
            gr.Markdown("### 💬 Conversations")
            conversations_table = gr.Dataframe(
                headers=["created_at", "user_input", "assistant_reply"],
                datatype=["str", "str", "str"],
                interactive=False
            )

    ui.load(
        fn=lambda: (load_notes(), load_conversations()),
        outputs=[notes_table, conversations_table],
    )
    state_store = gr.State()

    send_btn.click(
        chat_fn,
        inputs=[user_input, chatbot],
        outputs=[chatbot, state_store, save_section, conversations_table],
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
    print("checking notes", load_notes())
    ui.launch()
