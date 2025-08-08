from agno.agent import Agent
from agents.base import create_model_instance
from storage.loader import load_session_storage



def create_main_agent(provider, model_name, api_key, _personality_agent, _task_agent):
    return Agent(
        name="Main Agent",
        role="Talk to the user and delegate to other agents.",
        model=create_model_instance(provider, model_name, api_key),
        add_history_to_messages=True,
        storage=load_session_storage(),
        team=[_personality_agent, _task_agent],
        instructions="""
            Talk to the user naturally and helpfully.
            Provide complete, well-formatted responses.
            When including mathematical expressions, use proper LaTeX formatting:
            - Use \\( expression \\) for inline math
            - Use \\[ expression \\] for display math
            Do not mention delegation or other agents.
        """,
        markdown=True,
        stream=False,
    )
