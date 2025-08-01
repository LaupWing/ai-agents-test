from config import MODEL_GPT_4O
from google.adk.agents import Agent
from agents.greeting_agent.agent import greeting_agent
from agents.farwell_agent.agent import farewell_agent

def get_weather(city: str) -> dict:
    city_normalized = city.lower().replace(" ", "")
    mock_weather_db = {
        "newyork": {"status": "success", "report": "Sunny in New York, 25°C"},
        "london": {"status": "success", "report": "Cloudy in London, 15°C"},
        "tokyo": {"status": "success", "report": "Rainy in Tokyo, 18°C"},
    }
    return mock_weather_db.get(city_normalized, {
        "status": "error",
        "error_message": f"Sorry, I don't have weather info for {city}."
    })


if greeting_agent and farewell_agent:
    root_agent_model = MODEL_GPT_4O 

    weather_agent_team = Agent(
        name="weather_agent_v2",
        model=MODEL_GPT_4O,
        description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
        instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                    "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                    "You have specialized sub-agents: "
                    "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                    "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                    "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                    "If it's a weather request, handle it yourself using 'get_weather'. "
                    "For anything else, respond appropriately or state you cannot handle it.",
        tools=[get_weather], # Root agent still needs the weather tool for its core task
        # Key change: Link the sub-agents here!
        sub_agents=[greeting_agent, farewell_agent]
    )
    print(f"✅ Root Agent '{weather_agent_team.name}' created using model '{root_agent_model}' with sub-agents: {[sa.name for sa in weather_agent_team.sub_agents]}")

else:
    print("❌ Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
    if not greeting_agent: print(" - Greeting Agent is missing.")
    if not farewell_agent: print(" - Farewell Agent is missing.")
    if 'get_weather' not in globals(): print(" - get_weather function is missing.")