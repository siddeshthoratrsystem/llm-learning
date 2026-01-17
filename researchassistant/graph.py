from langgraph.checkpoint.memory import MemorySaver
from researchassistant.nodes.research_manager import research_manager_node
from langgraph.constants import END, START
from researchassistant.state.state import ResearchAssistantState
from langgraph.graph.state import StateGraph


graph = StateGraph(ResearchAssistantState)
checkpointer = MemorySaver()


graph.add_node("research_manager", research_manager_node)
graph.set_entry_point("research_manager")
graph.add_edge("research_manager", END)

# 4️⃣ Compile
config = {"configurable": {"thread_id": "user-1"}}
graph = graph.compile(checkpointer=checkpointer)

print("✅ Graph compiled successfully")

initial_state: ResearchAssistantState = {
    "topic": "",
    "researched_output": ""
}

graph.invoke(initial_state, config=config)

# Later create a separate file for this
import gradio as gr
# =========================================================
# GRADIO UI
# =========================================================

def chat(user_input, history):

    print("User input:", user_input)
    result = graph.invoke(
        {
            "topic": user_input,
            "researched_output": ""
        },
        config=config
    )
    print(result)
    return result['researched_output']

gr.ChatInterface(
    chat,
    title="LangGraph Chatbot"
).launch()
