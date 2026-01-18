from research_assistant.app.graph.state import GraphState
from research_assistant.app.memory.vector_store import save_note

def save_note_handler(state: GraphState):
    print("Executing save_note_handler with interrupt response:", state)
    if state.get("interrupt_response") == "confirm":
        # Save to Chroma
        save_note(state["final_answer"])
        print("Note saved:", state["final_answer"])

    # cancel = do nothing
    return state
