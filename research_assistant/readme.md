# 🧠 Research Assistant (LangGraph + Gradio)

A stateful, human-in-the-loop (HITL) research assistant built using **LangGraph**, **Gradio**, and **ChromaDB**.  
The assistant supports streaming responses, approval-based actions (like saving notes), persistent memory, and observability via LangSmith.

---

## ✨ Features

- 💬 Chat-based UI with streaming responses
- 🧵 Stateful execution using LangGraph
- ✋ Human-in-the-loop approval flows (Save / Confirm / Cancel)
- 📝 Save conversations and notes to ChromaDB
- 📊 View saved notes and conversations in tables
- 🔁 Resume graph execution after interrupts
- 🧠 Thread-aware memory (`thread_id`)
- 🔍 Observability & tracing via LangSmith

---

## 🏗️ Architecture Overview

```text
User (Gradio UI)
   ↓
LangGraph (State Machine)
   ├─ Input Router
   ├─ Agent / ReAct Loop
   ├─ Tool Calls (Search, etc.)
   ├─ Save Note Gate (Interrupt)
   ├─ Save Note Handler
   ↓
ChromaDB (Notes & Conversations)

```

## 🏗️ Project Structure

```
research_assistant/
├── app/
│   ├── graph/
│   │   ├── edges.py          # Graph definition
│   │   ├── nodes.py          # Agent, tools, save handlers
│   │   ├── state.py          # Graph state
│   ├── memory/
│   │   ├── vector_store.py         # ChromaDB setup
│   ├── tools/
│   │   ├── web_search.py         # Web Search using GoogleSerperAPIWrapper
│   │   ├── calendar.py         # calendar
│   ├── ui/
│   │   ├── gradio.py         # Gradio UI
│
├── .env
├── requirements.txt
└── README.md
```


## 🧠 State Design

```
class GraphState(TypedDict, total=False):
    user_input: str
    messages: list
    final_answer: str
    thread_id: str

    save_note_requested: bool
    interrupt_response: Literal["confirm", "cancel"]
```

## 🧠 🔍 Observability (LangSmith)

LangSmith is used for:
- Tracing LangGraph execution
- Debugging interrupts
- Inspecting node transitions
- Viewing LLM & tool calls

## 🚀 Running the App

```
python -m research_assistant.app.ui.gradio
```