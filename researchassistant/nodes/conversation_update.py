# researchassistant/nodes/conversation_update.py
from researchassistant.state.state import ResearchAssistantState

def update_conversation_history_node(
    state: ResearchAssistantState
) -> ResearchAssistantState:
    """
    Appends the latest user + assistant turn to conversation history.
    """

    user_msg = f"USER: {state['topic']}"
    assistant_msg = f"ASSISTANT: {state['researched_output']}"

    state["conversation_history"].append(user_msg)
    state["conversation_history"].append(assistant_msg)

    return state
