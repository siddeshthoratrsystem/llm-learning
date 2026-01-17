from researchassistant.prompts.get_research_prompt import get_research_prompt
from aiohttp.web_routedef import get
from researchassistant.llm.openai import LLMClient
from researchassistant.state.state import ResearchAssistantState

def research_manager_node(state: ResearchAssistantState):
    print("Managing research tasks")

    # call an LLM to perform research
    llm_client = LLMClient()
    prompt = get_research_prompt(state["topic"])
    response = llm_client.llm.invoke([{"role": "user", "content": prompt}])

    raw_research = response.content
    
    state["researched_output"] = raw_research

    return state