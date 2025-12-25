from langchain_community.llms import Ollama

def get_llm():
    return Ollama(
        model="phi3:mini",
        temperature=0,
        num_ctx=2048
    )
