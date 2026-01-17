def get_research_prompt(topic: str) -> str:
    return f"""
    You are a research assistant.

    Research the following topic and produce a concise, factual summary.
    Avoid opinions. Be structured.

    Topic:
    "{topic}"
    """

def extract_fact_prompt(research_text: str) -> str:
    return f"""
    You are a fact extractor.

    Extract factual statements from the text below.
    Return ONLY a valid JSON array of strings.
    Do NOT use markdown.
    Do NOT add explanations.
    Do NOT wrap in ```.

    Text:
    "{research_text}"
    """