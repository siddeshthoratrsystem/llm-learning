from researchassistant.memory.chroma import vectorstore

def load_all_facts(limit: int = 50):
    """
    Load facts for UI display.
    """
    """
    Load all facts stored in the vector DB.

    Returns:
        List[str]: list of fact strings
    """

    # Access the underlying Chroma collection
    collection = vectorstore._collection

    results = collection.get(limit=limit)

    # `documents` is a list of strings
    facts = results.get("documents", [])

    return facts
