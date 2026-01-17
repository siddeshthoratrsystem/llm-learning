# researchassistant/nodes/conversation_store.py
from researchassistant.state.state import ResearchAssistantState
# from researchassistant.memory.chroma import conversation_collection

def store_conversation_node(
    state: ResearchAssistantState
) -> ResearchAssistantState:
    print("💾 Storing conversation")

    # for i, msg in enumerate(state["conversation_history"]):
    #     conversation_collection.add(
    #         documents=[msg],
    #         ids=[f"{state['conversation_id']}_msg_{i}"],
    #         metadatas=[{
    #             "conversation_id": state["conversation_id"]
    #         }]
    #     )

    return state
