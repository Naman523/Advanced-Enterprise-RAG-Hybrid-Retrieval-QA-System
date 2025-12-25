from llm.local_llm import get_llm

_llm = get_llm()

def expand_query(query: str):
    # If query is already descriptive, skip expansion
    if len(query.split()) >= 4:
        return [query]

    prompt = f"""
    Generate 3 alternative search queries for:
    {query}
    """
    try:
        result = _llm.invoke(prompt)
        queries = [q.strip("- ").strip() for q in result.split("\n") if q.strip()]
        return list(set([query] + queries))
    except Exception:
        return [query]
