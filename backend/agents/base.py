from agno.models.perplexity import Perplexity
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
def create_model_instance(provider, model_name, api_key):
    if provider == "Perplexity":
        return Perplexity(id=model_name, api_key=api_key)
    elif provider == "Groq":
        return Groq(id=model_name, api_key=api_key)
    elif provider == "OpenAI":
        return OpenAIChat(id=model_name, api_key=api_key)
