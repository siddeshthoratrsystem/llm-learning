def get_research_prompt(topic: str) -> str:
    return f"""
    You are a research assistant.

    Research the following topic and produce a concise, factual summary.
    Avoid opinions. Be structured.

    Topic:
    "{topic}"
    """