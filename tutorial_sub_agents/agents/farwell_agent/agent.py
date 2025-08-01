from config import MODEL_GPT_4O
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."

farewell_agent = None
try:
    farewell_agent = Agent(
        model = LiteLlm(model=MODEL_GPT_4O),
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
            "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
            "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
            "Do not perform any other actions.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
        tools=[say_goodbye],
    )
    print(f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Farewell agent. Check API Key ({farewell_agent.model}). Error: {e}")