from agno.agent import Agent
from agents.base import create_model_instance
from storage.loader import load_personality_storage

def create_personality_agent(provider, model_name, api_key):
    return Agent(
        name="Personality Agent",
        role="Summarize the conversation and identify personality traits.",
        model=create_model_instance(provider, model_name, api_key),
        add_history_to_messages=True,
        storage=load_personality_storage(),
        instructions="""
            Summarize the conversation and provide a brief personality analysis.
            Use LaTeX formatting where needed:
            - \\( inline math \\)
            - \\[ display math \\]
        """,
        markdown=True,
        stream=False,
    )
