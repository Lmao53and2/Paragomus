from agno.agent import Agent
from backend.agents.base import create_model_instance
from backend.storage.loader import load_personality_storage
import json
import os

class PersonalityProfile:
    def __init__(self):
        self.traits = {}
        self.preferences = {}
        self.communication_style = {}
        self.ui_preferences = {}
        self.interaction_history = []
    
    def to_dict(self):
        return {
            "traits": self.traits,
            "preferences": self.preferences,
            "communication_style": self.communication_style,
            "ui_preferences": self.ui_preferences,
            "interaction_history": self.interaction_history[-10:]  # Keep last 10 interactions
        }
    
    def from_dict(self, data):
        self.traits = data.get("traits", {})
        self.preferences = data.get("preferences", {})
        self.communication_style = data.get("communication_style", {})
        self.ui_preferences = data.get("ui_preferences", {})
        self.interaction_history = data.get("interaction_history", [])

class DynamicPersonalityAgent:
    def __init__(self, provider, model_name, api_key):
        self.agent = Agent(
            name="Dynamic Personality Agent",
            role="Build and maintain dynamic user personality profiles for adaptive interactions.",
            model=create_model_instance(provider, model_name, api_key),
            add_history_to_messages=True,
            storage=load_personality_storage(),
            instructions="""
                You are a dynamic personality analysis agent. Your role is to:
                1. Analyze user interactions to build a comprehensive personality profile
                2. Update and refine the profile with each interaction
                3. Generate JSON output for other agents to consume
                4. Suggest UI adaptations based on personality insights
                
                For each analysis, provide a JSON response with these sections:
                - traits: Core personality traits (Big Five, communication style, etc.)
                - preferences: User preferences for interaction, content, format
                - communication_style: How the user prefers to communicate
                - ui_preferences: Suggested UI adaptations (colors, layout, complexity)
                - confidence_scores: How confident you are in each assessment (0-1)
                
                Always maintain and update the existing profile rather than starting fresh.
                Focus on actionable insights that can improve user experience.
            """,
            markdown=False,
            stream=False,
        )
        self.profile = PersonalityProfile()
        self.profile_file = "user_personality_profile.json"
        self.load_profile()
    
    def load_profile(self):
        """Load existing personality profile from file."""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r') as f:
                    data = json.load(f)
                    self.profile.from_dict(data)
            except Exception as e:
                print(f"Warning: Could not load personality profile: {e}")
    
    def save_profile(self):
        """Save personality profile to file."""
        try:
            with open(self.profile_file, 'w') as f:
                json.dump(self.profile.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save personality profile: {e}")
    
    def analyze_and_update(self, user_input, assistant_response=""):
        """Analyze interaction and update personality profile."""
        # Create analysis prompt with current profile context
        current_profile = json.dumps(self.profile.to_dict(), indent=2)
        
        analysis_prompt = f"""
        Current User Profile:
        {current_profile}
        
        New Interaction:
        User: {user_input}
        Assistant: {assistant_response}
        
        Please analyze this interaction and update the personality profile. 
        Return ONLY a valid JSON object with the updated profile including:
        {{
            "traits": {{
                "openness": 0.0-1.0,
                "conscientiousness": 0.0-1.0,
                "extraversion": 0.0-1.0,
                "agreeableness": 0.0-1.0,
                "neuroticism": 0.0-1.0,
                "communication_directness": 0.0-1.0,
                "technical_aptitude": 0.0-1.0
            }},
            "preferences": {{
                "detail_level": "high/medium/low",
                "response_length": "brief/moderate/detailed",
                "formality": "casual/professional/mixed",
                "examples_preferred": true/false
            }},
            "communication_style": {{
                "tone": "friendly/professional/direct/supportive",
                "pace": "fast/moderate/slow",
                "complexity": "simple/moderate/complex"
            }},
            "ui_preferences": {{
                "color_scheme": "light/dark/auto",
                "layout": "minimal/standard/detailed",
                "animation_level": "none/subtle/full",
                "information_density": "low/medium/high"
            }},
            "confidence_scores": {{
                "traits": 0.0-1.0,
                "preferences": 0.0-1.0,
                "communication_style": 0.0-1.0,
                "ui_preferences": 0.0-1.0
            }}
        }}
        """
        
        try:
            response = self.agent.run(analysis_prompt)
            response_text = response.content if hasattr(response, "content") else str(response)
            
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                updated_profile = json.loads(json_str)
                
                # Update profile with new data
                self.profile.from_dict(updated_profile)
                
                # Add interaction to history
                self.profile.interaction_history.append({
                    "user_input": user_input[:200],  # Truncate for storage
                    "assistant_response": assistant_response[:200],
                    "timestamp": str(os.times())
                })
                
                # Save updated profile
                self.save_profile()
                
                return self.profile.to_dict()
            else:
                print("Warning: Could not extract JSON from personality analysis")
                return self.profile.to_dict()
                
        except Exception as e:
            print(f"Error in personality analysis: {e}")
            return self.profile.to_dict()
    
    def get_profile_json(self):
        """Get current personality profile as JSON."""
        return self.profile.to_dict()
    
    def get_adaptation_suggestions(self):
        """Get specific suggestions for adapting other agents and UI."""
        profile = self.profile.to_dict()
        
        suggestions = {
            "task_agent_adaptations": {
                "task_format": "detailed" if profile.get("preferences", {}).get("detail_level") == "high" else "brief",
                "priority_emphasis": "high" if profile.get("traits", {}).get("conscientiousness", 0.5) > 0.7 else "moderate",
                "deadline_sensitivity": "high" if profile.get("traits", {}).get("neuroticism", 0.5) < 0.3 else "moderate"
            },
            "chat_agent_adaptations": {
                "response_tone": profile.get("communication_style", {}).get("tone", "friendly"),
                "response_length": profile.get("preferences", {}).get("response_length", "moderate"),
                "formality_level": profile.get("preferences", {}).get("formality", "mixed"),
                "include_examples": profile.get("preferences", {}).get("examples_preferred", True)
            },
            "ui_adaptations": profile.get("ui_preferences", {})
        }
        
        return suggestions

def create_personality_agent(provider, model_name, api_key):
    """Create the enhanced dynamic personality agent."""
    return DynamicPersonalityAgent(provider, model_name, api_key)
