from langgraph.graph.message import add_messages
from typing import TypedDict, List, Optional, Any


class GraphState(TypedDict, total=False):
    user_input: str
    intent: str
    messages: List[Any]
    tool_result: str
    draft_note: str
    approved_note: str
    final_answer: str

    save_note_requested: bool
    interrupt_response: Optional[str]  # "confirm" | "cancel"
