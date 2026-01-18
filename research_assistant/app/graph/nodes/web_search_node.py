from research_assistant.app.tools.web_search import web_search

def web_search_node(state):
    print("Executing web_search_node with input:", state["user_input"])
    result = web_search(state["user_input"])
    return {**state, "tool_result": result, "next_action": "react_agent"}