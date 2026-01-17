from researchassistant.memory.chroma import vectorstore
import json
from researchassistant.prompts.prompts import extract_fact_prompt
from aiohttp.web_routedef import get
from researchassistant.llm.openai import LLMClient
from researchassistant.state.state import ResearchAssistantState

def extract_and_store_fact_node(state: ResearchAssistantState):
    print("Entered into fact extractor node")

    # call an LLM to perform research
    llm_client = LLMClient()
    prompt = extract_fact_prompt(state["researched_output"])
    facts = llm_client.llm.invoke([{"role": "user", "content": prompt}]).content.strip()

    if not facts:
        return
    for fact in facts.split("\n"):
        vectorstore.add_texts([fact])
    
    return state


