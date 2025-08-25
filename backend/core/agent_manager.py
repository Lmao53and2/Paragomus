from agents.main_agent import create_main_agent
from agents.task_agent import create_task_agent
from agents.personality_agent import create_personality_agent
from agents.ui_agent import create_ui_agent
import json

class AgentManager:
    def __init__(self, provider, model, api_key):
        # Initialize all agents
        self.personality_agent = create_personality_agent(provider, model, api_key)
        self.task_agent = create_task_agent(provider, model, api_key)
        self.main_agent = create_main_agent(provider, model, api_key, self.personality_agent, self.task_agent)
        self.ui_agent = create_ui_agent(provider, model, api_key)
        
        # Current personality profile and adaptations
        self.current_personality_profile = {}
        self.current_adaptations = {}
        self.current_ui_config = {}

    def ask(self, prompt, context=""):
        """Generate a personality-adapted response."""
        # Update personality profile based on this interaction
        personality_data = self.personality_agent.analyze_and_update(prompt)
        self.current_personality_profile = personality_data
        
        # Get adaptation suggestions
        adaptations = self.personality_agent.get_adaptation_suggestions()
        self.current_adaptations = adaptations
        
        # Update agents with personality context
        self.main_agent.update_personality_context(personality_data)
        self.task_agent.update_personality_context(personality_data)
        self.ui_agent.update_personality_context(personality_data)
        
        # Generate adapted response
        chat_adaptations = adaptations.get("chat_agent_adaptations", {})
        response = self.main_agent.generate_response(prompt, context, chat_adaptations)
        
        # Update personality profile with the assistant's response
        self.personality_agent.analyze_and_update(prompt, response)
        
        return response

    def extract_tasks(self, prompt):
        """Extract tasks with personality adaptations."""
        task_adaptations = self.current_adaptations.get("task_agent_adaptations", {})
        return self.task_agent.extract_tasks(prompt, task_adaptations)

    def analyze_personality(self, user_input, assistant_response=""):
        """Analyze and update personality profile."""
        return self.personality_agent.analyze_and_update(user_input, assistant_response)
    
    def get_personality_profile(self):
        """Get current personality profile."""
        return self.current_personality_profile
    
    def get_ui_config(self, context=""):
        """Generate UI configuration based on current personality profile."""
        ui_adaptations = self.current_adaptations.get("ui_adaptations", {})
        ui_config = self.ui_agent.generate_ui_config(context, ui_adaptations)
        self.current_ui_config = ui_config
        return ui_config
    
    def get_adaptation_suggestions(self):
        """Get current adaptation suggestions for all agents."""
        return self.current_adaptations
    
    def get_full_context(self):
        """Get complete context including personality, adaptations, and UI config."""
        return {
            "personality_profile": self.current_personality_profile,
            "adaptations": self.current_adaptations,
            "ui_config": self.current_ui_config,
            "timestamp": str(__import__('time').time())
        }
