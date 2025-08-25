from agno.agent import Agent
from backend.agents.base import create_model_instance
from backend.storage.loader import load_session_storage
import json

class GenerativeUIAgent:
    def __init__(self, provider, model_name, api_key):
        self.agent = Agent(
            name="Generative UI Agent",
            role="Generate adaptive UI configurations based on user personality and context.",
            model=create_model_instance(provider, model_name, api_key),
            add_history_to_messages=True,
            storage=load_session_storage(),
            instructions="""
                You are a generative UI agent that creates adaptive user interfaces based on personality profiles.
                Generate UI configurations, component layouts, and styling that match user preferences and personality traits.
                
                Your responses should include:
                - Component configurations
                - Layout suggestions
                - Color schemes and themes
                - Interaction patterns
                - Information architecture
                
                Always return valid JSON configurations that can be consumed by React components.
            """,
            markdown=False,
            stream=False,
        )
        self.personality_profile = {}
    
    def update_personality_context(self, personality_data):
        """Update the personality context for UI generation."""
        self.personality_profile = personality_data
    
    def generate_ui_config(self, context="", ui_adaptations=None):
        """Generate UI configuration based on personality and context."""
        if ui_adaptations is None:
            ui_adaptations = {}
        
        # Build personality-aware UI generation prompt
        adaptation_context = ""
        if ui_adaptations:
            color_scheme = ui_adaptations.get("color_scheme", "auto")
            layout = ui_adaptations.get("layout", "standard")
            animation_level = ui_adaptations.get("animation_level", "subtle")
            info_density = ui_adaptations.get("information_density", "medium")
            
            adaptation_context = f"""
            User UI Preferences:
            - Color Scheme: {color_scheme}
            - Layout Style: {layout}
            - Animation Level: {animation_level}
            - Information Density: {info_density}
            
            Generate UI configuration accordingly:
            - Color scheme should be {color_scheme}
            - Layout should be {layout} (minimal=clean/simple, standard=balanced, detailed=information-rich)
            - Animations should be {animation_level} (none=static, subtle=smooth transitions, full=rich animations)
            - Information density should be {info_density} (low=spacious, medium=balanced, high=compact)
            """
        
        full_prompt = f"""
        {adaptation_context}
        
        Context: {context}
        
        Generate a comprehensive UI configuration JSON that includes:
        1. Theme configuration (colors, typography, spacing)
        2. Layout configuration (component arrangement, grid system)
        3. Component configurations (chat interface, task display, personality insights)
        4. Interaction patterns (animations, transitions, feedback)
        5. Responsive behavior
        
        Return ONLY a valid JSON object with this structure:
        {{
            "theme": {{
                "colorScheme": "light/dark/auto",
                "primaryColor": "#hex",
                "secondaryColor": "#hex",
                "backgroundColor": "#hex",
                "textColor": "#hex",
                "accentColor": "#hex"
            }},
            "layout": {{
                "type": "minimal/standard/detailed",
                "sidebar": true/false,
                "headerStyle": "compact/standard/prominent",
                "contentLayout": "single-column/two-column/three-column"
            }},
            "components": {{
                "chatInterface": {{
                    "style": "bubble/linear/card",
                    "showTimestamps": true/false,
                    "showPersonalityInsights": true/false,
                    "messageSpacing": "compact/normal/spacious"
                }},
                "taskDisplay": {{
                    "viewType": "list/grid/kanban",
                    "showPriority": true/false,
                    "showDeadlines": true/false,
                    "groupBy": "priority/category/date"
                }},
                "personalityPanel": {{
                    "visible": true/false,
                    "position": "sidebar/modal/inline",
                    "detailLevel": "summary/detailed/full"
                }}
            }},
            "animations": {{
                "level": "none/subtle/full",
                "transitionDuration": "fast/normal/slow",
                "enableHover": true/false,
                "enablePageTransitions": true/false
            }},
            "responsive": {{
                "breakpoints": {{"mobile": 768, "tablet": 1024, "desktop": 1200}},
                "mobileLayout": "stack/tabs/drawer",
                "adaptiveComponents": true/false
            }}
        }}
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
                # Fallback to default configuration
                return self.get_default_ui_config()
                
        except Exception as e:
            print(f"Error in UI generation: {e}")
            return self.get_default_ui_config()
    
    def get_default_ui_config(self):
        """Return a default UI configuration."""
        return {
            "theme": {
                "colorScheme": "auto",
                "primaryColor": "#3b82f6",
                "secondaryColor": "#64748b",
                "backgroundColor": "#ffffff",
                "textColor": "#1f2937",
                "accentColor": "#10b981"
            },
            "layout": {
                "type": "standard",
                "sidebar": True,
                "headerStyle": "standard",
                "contentLayout": "two-column"
            },
            "components": {
                "chatInterface": {
                    "style": "bubble",
                    "showTimestamps": True,
                    "showPersonalityInsights": True,
                    "messageSpacing": "normal"
                },
                "taskDisplay": {
                    "viewType": "list",
                    "showPriority": True,
                    "showDeadlines": True,
                    "groupBy": "priority"
                },
                "personalityPanel": {
                    "visible": True,
                    "position": "sidebar",
                    "detailLevel": "summary"
                }
            },
            "animations": {
                "level": "subtle",
                "transitionDuration": "normal",
                "enableHover": True,
                "enablePageTransitions": True
            },
            "responsive": {
                "breakpoints": {"mobile": 768, "tablet": 1024, "desktop": 1200},
                "mobileLayout": "stack",
                "adaptiveComponents": True
            }
        }
    
    def generate_component_config(self, component_type, context=""):
        """Generate specific component configuration."""
        prompt = f"""
        Generate a specific configuration for a {component_type} component.
        Context: {context}
        
        Return a JSON configuration optimized for the user's personality profile.
        """
        
        try:
            response = self.agent.run(prompt)
            response_text = response.content if hasattr(response, "content") else str(response)
            
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"error": "Could not generate component configuration"}
                
        except Exception as e:
            print(f"Error generating component config: {e}")
            return {"error": str(e)}

def create_ui_agent(provider, model_name, api_key):
    """Create the generative UI agent."""
    return GenerativeUIAgent(provider, model_name, api_key)