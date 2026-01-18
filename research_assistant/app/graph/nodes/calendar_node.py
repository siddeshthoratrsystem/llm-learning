from research_assistant.app.tools.calendar import calendar

def calendar_node(state):
    print("Calendar node received state:", state)
    result = calendar(state["user_input"])
    return {**state, "tool_result": result, "next_action": "react_agent"}