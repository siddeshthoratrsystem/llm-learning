
# go in node file
from langgraph.types import interrupt
from research_assistant.app.graph.state import GraphState
def save_note_gate(state: GraphState):

    print("Executing save_note_gate with final answer:", state)
    if not state.get("save_note_requested") or state.get("interrupt_response") in ["confirm", "cancel"]:
        return state

    print("Prompting user to save note...")
    response = interrupt(
        {
            "question": "Do you want to save this reply as a note?",
            "note": state["final_answer"],
        }
    )

    print("Interrupt response:", response)
    state["interrupt_response"] = response  # "confirm" | "cancel"

    return state