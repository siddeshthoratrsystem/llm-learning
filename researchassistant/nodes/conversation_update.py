# researchassistant/nodes/conversation_update.py
from researchassistant.state.state import ResearchAssistantState
from researchassistant.memory.chroma import conversation_store

def update_conversation_history_node(
    state: ResearchAssistantState
) -> ResearchAssistantState:
    """
    Appends the latest user + assistant turn to conversation history.
    """

    user_msg = f"{state['topic']}"
    assistant_msg = f"{state['researched_output']}"

    conversation_store.add_texts(
        [user_msg]
    )

    conversation_store.add_texts(
        [assistant_msg]
    )

    state["conversation_history"].append(user_msg)
    state["conversation_history"].append(assistant_msg)

    return state
