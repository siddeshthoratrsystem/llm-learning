from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def react_agent(state):
    print("Executing react_agent")

    tool_result = state.get("tool_result")

    if tool_result:
        observation = f"Observation: {tool_result}"
    else:
        observation = ""

    prompt = f"""
    You are a ReAct agent. Interpret the user query and the observation from the last tool use (if any) to 
    decide your next action. If the user query has been sufficiently answered and you have used web_search tool,
    save it to notes and then choose the finish action and provide a final answer. If web_search is not used and still the query
    is sufficiently answered, just choose finish and provide the final answer.Otherwise, choose an appropriate tool to gather more information.

    User Query:
    {state["user_input"]}

    {observation}

    Decide the next step.

    You may choose ONE action if applicable from the following tools:
    - web_search: Use web search tool ONLY when researching for a particular topic or looking for up-to-date information.
    - finish

    Respond EXACTLY in this format:

    Thought: <your reasoning>
    Action: <one action from above>
    Answer: <only if action is finish>
    """

    response = llm.invoke(prompt).content
    print("LLM response:\n", response)

    # --- Robust parsing ---
    thought = response.split("Thought:")[1].split("Action:")[0].strip()
    action = response.split("Action:")[1].split("\n")[0].strip()
    answer = None

    if "Answer:" in response:
        answer = response.split("Answer:")[1].strip()

    print("Parsed action:", action)

    # --- State transitions ---
    if action == "finish":
        return {
            **state,
            "final_answer": answer,
            "next_action": "finish"
        }

    print("next_action", action)
    # Tool actions (NO ANSWER HERE)
    return {
        **state,
        "next_action": action
    }
