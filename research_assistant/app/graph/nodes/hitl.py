from langgraph.types import interrupt

def hitl_approval(state):
    print("Executing HITL approval with draft note:", state["draft_note"])
    # decision = interrupt(
    #     {
    #         "question": "Approve this note?",
    #         "note": state["draft_note"]
    #     }
    # )

    # if decision["approved"]:
    #     return {**state, "approved_note": state["draft_note"], "next_action": "react_agent", "decision": "approved"}
    # else:
    return state
