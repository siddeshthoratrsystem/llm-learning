from research_assistant.app.tools.note_draft import note_draft

def note_draft_node(state):
    print("Executing note_draft_node with input:", state["user_input"])
    result = note_draft(state["user_input"])
    return {**state, "draft_note": result}