from agno.agent import Agent
from agents.base import create_model_instance
from storage.loader import load_task_storage

def create_task_agent(provider, model_name, api_key):
    return Agent(
        name="Task Agent",
        role="Extract tasks from the conversation.",
        model=create_model_instance(provider, model_name, api_key),
        add_history_to_messages=True,
        storage=load_task_storage(),
        instructions="""
            Extract actionable tasks. Return as list, one per line starting with '- '.
            Use proper LaTeX formatting:
            - \\( inline math \\)
            - \\[ display math \\]
        """,
        markdown=True,
        stream=False,
    )
