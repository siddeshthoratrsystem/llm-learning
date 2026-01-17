from typing import List, TypedDict

class ResearchAssistantState(TypedDict):
    topic: str
    researched_output: str

    conversation_id: str
    conversation_history: List[str]