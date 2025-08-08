from agents.base import create_model_instance
from agents.main_agent import create_main_agent
from agents.task_agent import create_task_agent
from agents.personality_agent import create_personality_agent
from utils.pdf_parser import extract_text_from_pdf
from services.task_extraction import parse_tasks_from_response
from dotenv import load_dotenv
import os
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
    print(f"✅ Agent initialized: {type(agent.main_agent.model)}")
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


def parse_personality_traits_from_response(response_text):
    """Parse personality traits from the personality agent's response."""
    traits = []
    lines = response_text.split('\n')
    
    # Look for common personality analysis patterns
    trait_indicators = [
        'trait:', 'personality:', 'characteristic:', 'tendency:', 
        'shows:', 'indicates:', 'demonstrates:', 'exhibits:',
        'appears to be:', 'seems to:', 'likely to:'
    ]
    
    for line in lines:
        line_lower = line.lower().strip()
        for indicator in trait_indicators:
            if indicator in line_lower:
                trait = line.replace(indicator, '').strip()
                if trait and len(trait) > 5:  # Filter out very short matches
                    traits.append(trait.capitalize())
    
    # Also look for bullet points or numbered lists that might contain traits
    if not traits:
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*')) or (line and line[0].isdigit() and '.' in line):
                clean_line = line.lstrip('•-*0123456789. ').strip()
                if clean_line and len(clean_line) > 10:
                    traits.append(clean_line)
    
    return traits[:5]  # Limit to top 5 traits for readability


def display_extracted_tasks(agent, user_input):
    """Extract and display tasks from user input."""
    print("\n--- 📋 Extracted Tasks ---")
    
    try:
        task_response = agent.extract_tasks(user_input)
        task_text = task_response.content if hasattr(task_response, "content") else str(task_response)
        parsed_tasks = parse_tasks_from_response(task_text)
        
        if parsed_tasks:
            for i, task in enumerate(parsed_tasks, 1):
                print(f"🔹 Task {i}: {task}")
        else:
            print("❌ No clear tasks found")
            
    except Exception as e:
        print(f"❌ Error extracting tasks: {e}")


def display_personality_insights(agent, user_input, assistant_response):
    """Extract and display personality traits from the conversation."""
    print("\n--- 🧠 Personality Insights ---")
    
    try:
        # Create a conversation context for the personality agent
        conversation_context = f"User: {user_input}\nAssistant: {assistant_response}"
        
        # Call the personality analysis (assuming AgentManager has this method)
        if hasattr(agent, 'analyze_personality'):
            personality_response = agent.analyze_personality(conversation_context)
        elif hasattr(agent, 'personality_agent'):
            # Direct call to personality agent if available
            personality_response = agent.personality_agent.run(conversation_context)
        else:
            print("❌ Personality analysis not available")
            return
            
        personality_text = personality_response.content if hasattr(personality_response, "content") else str(personality_response)
        
        # Parse personality traits from the response
        personality_traits = parse_personality_traits_from_response(personality_text)
        
        if personality_traits:
            for i, trait in enumerate(personality_traits, 1):
                print(f"🧩 Trait {i}: {trait}")
        else:
            # If no traits found, show the raw analysis
            print(f"📝 Analysis: {personality_text[:200]}..." if len(personality_text) > 200 else personality_text)
            
    except Exception as e:
        print(f"❌ Error analyzing personality: {e}")


def chat_loop(agent, context_text):
    """Main chat loop with task and personality extraction."""
    print("💬 Ask me anything (type 'exit' to quit):\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
            
        try:
            # Get main response
            response = agent.ask(user_input, context=context_text)
            main_response = response.content if hasattr(response, "content") else str(response)
            
            print(f"🤖: {main_response}")
            
            # Display extracted tasks
            display_extracted_tasks(agent, user_input)
            
            # Display personality insights with both user input and assistant response
            display_personality_insights(agent, user_input, main_response)
            
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error during conversation: {e}")
            continue


def main():
    """Main application entry point."""
    print("🚀 Starting AI Assistant with Task & Personality Analysis")
    print("="*60)
    
    try:
        # Setup and initialization
        setup_providers()
        agent = initialize_agent()
        context_text = load_pdf_context()
        
        print("\n" + "="*60)
        
        # Start the chat loop
        chat_loop(agent, context_text)
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
