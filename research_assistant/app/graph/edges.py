from langgraph.checkpoint.memory import MemorySaver
from research_assistant.app.graph.nodes.note_draft_node import note_draft_node
from research_assistant.app.tools.note_draft import note_draft
from research_assistant.app.graph.nodes.hitl import hitl_approval
from research_assistant.app.graph.nodes.calendar_node import calendar_node
from calendar import calendar
from research_assistant.app.graph.nodes.web_search_node import web_search_node
from research_assistant.app.graph.nodes.react_agent import react_agent
from research_assistant.app.graph.nodes.input_router import input_router
from research_assistant.app.graph.state import GraphState
from langgraph.graph import StateGraph, END


def build_graph():
    graph = StateGraph(GraphState)
    checkpointer = MemorySaver()
    graph.add_node("input_router", input_router)
    graph.add_node("react_agent", react_agent)
    graph.add_node("web_search", web_search_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("note_draft", note_draft_node)
    graph.add_node("hitl", hitl_approval)


    graph.set_entry_point("input_router")
    graph.add_edge("input_router", "react_agent")
    

    # SIDTODO: unclear
    graph.add_conditional_edges(
        "react_agent",
        lambda s: s["next_action"],
        {"web_search": "web_search", "calendar": "calendar", "finish": END}
    )

    # SIDTODO: unclear
    graph.add_edge("web_search", "react_agent")
    graph.add_edge("react_agent", END)

    return graph.compile(checkpointer=checkpointer)
