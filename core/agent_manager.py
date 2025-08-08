from agents.main_agent import create_main_agent
from agents.task_agent import create_task_agent
from agents.personality_agent import create_personality_agent

class AgentManager:
    def __init__(self, provider, model, api_key):
        self.task_agent = create_task_agent(provider, model, api_key)
        self.personality_agent = create_personality_agent(provider, model, api_key)
        self.main_agent = create_main_agent(provider, model, api_key, self.personality_agent, self.task_agent)

    def ask(self, prompt, context=""):
        full_prompt = f"{context}\n\nUser: {prompt}" if context else prompt
        return self.main_agent.run(full_prompt)

    def extract_tasks(self, prompt):
        return self.task_agent.run(f"Extract tasks: {prompt}")

    def analyze_personality(self, prompt):
        return self.personality_agent.run(f"Analyze personality: {prompt}")
