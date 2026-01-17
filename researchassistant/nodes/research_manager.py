from researchassistant.prompts.prompts import get_research_prompt
from aiohttp.web_routedef import get
from researchassistant.llm.openai import LLMClient
from researchassistant.state.state import ResearchAssistantState

def research_manager_node(state: ResearchAssistantState):
    print("Managing research tasks")

    # call an LLM to perform research
    llm_client = LLMClient()
    prompt = get_research_prompt(state["topic"])

    # create a tool and pass it to llm modal, 
    # tool  name is fetch_stored_facts_for_provided_input
    # this tool will do similarity search in chromaDb vector and append it to the prompt
    
    response = llm_client.llm.invoke([{
        "role": "user", 
        "content": prompt
    }])

    raw_research = response.content
    
    state["researched_output"] = raw_research

    return state