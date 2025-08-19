from agno.agent import Agent
from agents.base import create_model_instance
from storage.loader import load_task_storage
import json

class AdaptiveTaskAgent:
    def __init__(self, provider, model_name, api_key):
        self.agent = Agent(
            name="Adaptive Task Agent",
            role="Extract and format tasks based on user personality and preferences.",
            model=create_model_instance(provider, model_name, api_key),
            add_history_to_messages=True,
            storage=load_task_storage(),
            instructions="""
                You are an adaptive task extraction agent. Extract actionable tasks from conversations
                and format them according to the user's personality profile and preferences.
                
                Always return tasks in JSON format with the following structure:
                {
                    "tasks": [
                        {
                            "title": "Task title",
                            "description": "Detailed description",
                            "priority": "high/medium/low",
                            "estimated_time": "time estimate",
                            "category": "work/personal/learning/etc",
                            "due_date": "suggested due date if applicable",
                            "subtasks": ["subtask1", "subtask2"] // if complex task
                        }
                    ],
                    "summary": "Brief summary of extracted tasks",
                    "recommendations": "Personalized recommendations based on user profile"
                }
            """,
            markdown=False,
            stream=False,
        )
        self.personality_profile = {}
    
    def update_personality_context(self, personality_data):
        """Update the personality context for task adaptation."""
        self.personality_profile = personality_data
    
    def extract_tasks(self, user_input, personality_adaptations=None):
        """Extract tasks with personality-based adaptations."""
        if personality_adaptations is None:
            personality_adaptations = {}
        
        # Build personality-aware prompt
        adaptation_context = ""
        if personality_adaptations:
            task_format = personality_adaptations.get("task_format", "moderate")
            priority_emphasis = personality_adaptations.get("priority_emphasis", "moderate")
            deadline_sensitivity = personality_adaptations.get("deadline_sensitivity", "moderate")
            
            adaptation_context = f"""
            User Personality Adaptations:
            - Task Detail Level: {task_format}
            - Priority Emphasis: {priority_emphasis}
            - Deadline Sensitivity: {deadline_sensitivity}
            
            Adapt your task extraction accordingly:
            - If detail_level is "high": Provide comprehensive descriptions and subtasks
            - If detail_level is "brief": Keep descriptions concise and focused
            - If priority_emphasis is "high": Clearly categorize and emphasize task priorities
            - If deadline_sensitivity is "high": Suggest specific deadlines and time management tips
            """
        
        full_prompt = f"""
        {adaptation_context}
        
        Extract actionable tasks from this user input: "{user_input}"
        
        Return ONLY a valid JSON object with the task structure specified in your instructions.
        """
        
        try:
            response = self.agent.run(full_prompt)
            response_text = response.content if hasattr(response, "content") else str(response)
            
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback to simple task extraction
                return {
                    "tasks": [{"title": "Process user request", "description": user_input}],
                    "summary": "Could not parse structured tasks",
                    "recommendations": "Please rephrase your request for better task extraction"
                }
                
        except Exception as e:
            print(f"Error in task extraction: {e}")
            return {
                "tasks": [],
                "summary": "Error in task extraction",
                "recommendations": "Please try again with a clearer request"
            }

def create_task_agent(provider, model_name, api_key):
    """Create the enhanced adaptive task agent."""
    return AdaptiveTaskAgent(provider, model_name, api_key)
