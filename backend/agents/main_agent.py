from agno.agent import Agent
from backend.agents.base import create_model_instance
from backend.storage.loader import load_session_storage
import json

class AdaptiveChatAgent:
    def __init__(self, provider, model_name, api_key):
        self.agent = Agent(
            name="Adaptive Chat Agent",
            role="Provide personalized conversational responses based on user personality.",
            model=create_model_instance(provider, model_name, api_key),
            add_history_to_messages=True,
            storage=load_session_storage(),
            instructions="""
                You are an adaptive conversational agent that personalizes responses based on user personality.
                Provide helpful, natural responses while adapting your communication style to match user preferences.
                
                Key adaptation areas:
                - Response tone and formality level
                - Level of detail and explanation
                - Use of examples and analogies
                - Technical complexity
                - Response length and structure
                
                Always be helpful and engaging while respecting the user's communication preferences.
            """,
            markdown=True,
            stream=False,
        )
        self.personality_profile = {}
    
    def update_personality_context(self, personality_data):
        """Update the personality context for response adaptation."""
        self.personality_profile = personality_data
    
    def generate_response(self, user_input, context="", personality_adaptations=None):
        """Generate personality-adapted response."""
        if personality_adaptations is None:
            personality_adaptations = {}
        
        # Build personality-aware prompt
        adaptation_context = ""
        if personality_adaptations:
            tone = personality_adaptations.get("response_tone", "friendly")
            length = personality_adaptations.get("response_length", "moderate")
            formality = personality_adaptations.get("formality_level", "mixed")
            examples = personality_adaptations.get("include_examples", True)
            
            adaptation_context = f"""
            User Communication Preferences:
            - Preferred Tone: {tone}
            - Response Length: {length}
            - Formality Level: {formality}
            - Include Examples: {examples}
            
            Adapt your response style accordingly:
            - Use a {tone} tone throughout your response
            - Keep responses {length} in length
            - Match the {formality} formality level
            - {"Include relevant examples and analogies" if examples else "Focus on direct answers without examples"}
            """
        
        full_prompt = f"""
        {adaptation_context}
        
        Context: {context}
        
        User: {user_input}
        
        Provide a helpful response adapted to the user's communication preferences.
        """
        
        try:
            response = self.agent.run(full_prompt)
            return response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            print(f"Error in chat response generation: {e}")
            return "I apologize, but I encountered an error processing your request. Please try again."

def create_main_agent(provider, model_name, api_key, _personality_agent, _task_agent):
    """Create the enhanced adaptive chat agent."""
    return AdaptiveChatAgent(provider, model_name, api_key)
