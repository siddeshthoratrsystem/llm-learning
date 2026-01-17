from researchassistant.nodes.store_conversation import store_conversation_node
from researchassistant.nodes.fact_extractor import extract_and_store_fact_node
from researchassistant.nodes.conversation_update import update_conversation_history_node
from langgraph.checkpoint.memory import MemorySaver
from researchassistant.nodes.research_manager import research_manager_node
from langgraph.constants import END, START
from researchassistant.state.state import ResearchAssistantState
from langgraph.graph.state import StateGraph


graph = StateGraph(ResearchAssistantState)
checkpointer = MemorySaver()


graph.add_node("research_manager", research_manager_node)
graph.add_node("update_conversation", update_conversation_history_node)
graph.add_node('fact_extractor', extract_and_store_fact_node)
graph.add_node('store_conversation', store_conversation_node)


graph.set_entry_point("research_manager")
graph.add_edge("research_manager", "update_conversation")
graph.add_edge("update_conversation", 'fact_extractor')
# graph.add_edge("fact_extractor", 'store_conversation')
# graph.add_edge("store_conversation", END)
graph.add_edge("fact_extractor", END)

# 4️⃣ Compile
graph = graph.compile(checkpointer=checkpointer)

print("✅ Graph compiled successfully")




