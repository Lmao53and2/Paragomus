from agents.base import create_model_instance
from agents.main_agent import create_main_agent
from agents.task_agent import create_task_agent
from agents.personality_agent import create_personality_agent
from agents.ui_agent import create_ui_agent
from utils.pdf_parser import extract_text_from_pdf
from services.task_extraction import parse_tasks_from_response
from dotenv import load_dotenv
import os
import json
from core.agent_manager import AgentManager
from agno.models.perplexity import Perplexity
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agents.model_registry import register_provider


def setup_providers():
    """Register all available AI model providers."""
    register_provider("perplexity", Perplexity)
    register_provider("openai", OpenAIChat)
    register_provider("groq", Groq)
    print("✅ Model providers registered successfully")


def initialize_agent():
    """Initialize the agent manager with environment configuration."""
    load_dotenv()
    
    provider = "Perplexity"
    model = "sonar"
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        raise ValueError("❌ PERPLEXITY_API_KEY not found in environment variables")
    
    agent = AgentManager(provider, model, api_key)
    print(f"✅ Enhanced Agent Manager initialized with 4 agents")
    return agent


def load_pdf_context():
    """Load PDF content if provided by user."""
    pdf_path = input("📎 Enter PDF path (or press Enter to skip): ").strip()
    
    if not pdf_path:
        return ""
    
    try:
        context_text = extract_text_from_pdf(pdf_path)
        print("✅ PDF loaded successfully")
        return context_text
    except Exception as e:
        print(f"❌ Failed to load PDF: {e}")
        return ""


def display_extracted_tasks(agent, user_input):
    """Extract and display tasks from user input with personality adaptations."""
    print("\n--- 📋 Extracted Tasks ---")
    
    try:
        task_data = agent.extract_tasks(user_input)
        
        if isinstance(task_data, dict):
            tasks = task_data.get('tasks', [])
            summary = task_data.get('summary', '')
            recommendations = task_data.get('recommendations', '')
            
            if tasks:
                for i, task in enumerate(tasks, 1):
                    print(f"🔹 Task {i}: {task.get('title', 'Untitled')}")
                    if task.get('description'):
                        print(f"   📝 {task['description']}")
                    if task.get('priority'):
                        print(f"   ⚡ Priority: {task['priority']}")
                    if task.get('estimated_time'):
                        print(f"   ⏱️  Time: {task['estimated_time']}")
                    print()
                
                if summary:
                    print(f"📊 Summary: {summary}")
                if recommendations:
                    print(f"💡 Recommendations: {recommendations}")
            else:
                print("❌ No tasks found")
        else:
            print("❌ Could not parse task data")
            
    except Exception as e:
        print(f"❌ Error extracting tasks: {e}")


def display_personality_insights(agent):
    """Display current personality profile and adaptations."""
    print("\n--- 🧠 Personality Insights ---")
    
    try:
        profile = agent.get_personality_profile()
        adaptations = agent.get_adaptation_suggestions()
        
        if profile.get('traits'):
            print("🧩 Key Traits:")
            for trait, value in profile['traits'].items():
                if value > 0.6:  # Only show strong traits
                    trait_name = trait.replace('_', ' ').title()
                    print(f"   • {trait_name}: {int(value * 100)}%")
        
        if profile.get('preferences'):
            print("\n🎯 Preferences:")
            for pref, value in profile['preferences'].items():
                pref_name = pref.replace('_', ' ').title()
                print(f"   • {pref_name}: {value}")
        
        if adaptations:
            print("\n🔧 Active Adaptations:")
            for agent_type, agent_adaptations in adaptations.items():
                agent_name = agent_type.replace('_adaptations', '').replace('_', ' ').title()
                print(f"   {agent_name}:")
                for key, value in agent_adaptations.items():
                    adaptation_name = key.replace('_', ' ').title()
                    print(f"     - {adaptation_name}: {value}")
            
    except Exception as e:
        print(f"❌ Error displaying personality insights: {e}")


def display_ui_config(agent):
    """Display current UI configuration."""
    print("\n--- 🎨 UI Configuration ---")
    
    try:
        ui_config = agent.get_ui_config()
        
        if ui_config.get('theme'):
            theme = ui_config['theme']
            print(f"🎨 Theme: {theme.get('colorScheme', 'auto')}")
            print(f"🎯 Primary Color: {theme.get('primaryColor', '#3b82f6')}")
        
        if ui_config.get('layout'):
            layout = ui_config['layout']
            print(f"📐 Layout: {layout.get('type', 'standard')}")
            print(f"📱 Content Layout: {layout.get('contentLayout', 'two-column')}")
        
        if ui_config.get('animations'):
            animations = ui_config['animations']
            print(f"✨ Animation Level: {animations.get('level', 'subtle')}")
            
    except Exception as e:
        print(f"❌ Error displaying UI config: {e}")


def chat_loop(agent, context_text):
    """Enhanced chat loop with full personality adaptation."""
    print("💬 Enhanced AI Assistant - Now with personality adaptation!")
    print("Ask me anything (type 'exit' to quit, 'profile' to see your personality):\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == 'profile':
            display_personality_insights(agent)
            display_ui_config(agent)
            print("\n" + "="*50 + "\n")
            continue
        
        if not user_input:
            continue
            
        try:
            # Get adaptive response (this automatically updates personality profile)
            response = agent.ask(user_input, context=context_text)
            
            print(f"🤖: {response}")
            
            # Display extracted tasks with adaptations
            display_extracted_tasks(agent, user_input)
            
            # Display updated personality insights
            display_personality_insights(agent)
            
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error during conversation: {e}")
            continue


def main():
    """Main application entry point."""
    print("🚀 Starting Enhanced Adaptive AI Assistant")
    print("="*60)
    print("Features:")
    print("• Dynamic personality profiling")
    print("• Adaptive task extraction")
    print("• Personalized responses")
    print("• Generative UI configuration")
    print("="*60)
    
    try:
        # Setup and initialization
        setup_providers()
        agent = initialize_agent()
        context_text = load_pdf_context()
        
        print("\n" + "="*60)
        
        # Start the enhanced chat loop
        chat_loop(agent, context_text)
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
