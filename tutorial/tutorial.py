import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.agents import Agent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService

load_dotenv()

session_service = InMemorySessionService()

# Constants
APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = str(uuid.uuid4())
AGENT_MODEL = "gemini-2.0-flash"
weather_agent_gpt = None    # Initialize to None
runner_gpt = None           # Initialize runner to None

async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default response

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                print(f"Final Response: {final_response_text}")
            else:
                print("No content in final response.")
            break;
    
    print(f"<<< Agent Response: {final_response_text}")

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
            Includes a 'status' key ('success' or 'error').
            If 'success', includes a 'report' key with weather details.
            If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---") # Log tool execution
    city_normalized = city.lower().replace(" ", "") # Basic normalization

    # Mock weather data
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}



# Async main
async def main():
    try:
        weather_agent = Agent(
            name="weather_agent_v1",
            model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
            description="Provides weather information for specific cities.",
            instruction="You are a helpful weather assistant. "
                        "When the user asks for the weather in a specific city, "
                        "use the 'get_weather' tool to find the information. "
                        "If the tool returns an error, inform the user politely. "
                        "If the tool is successful, present the weather report clearly.",
            tools=[get_weather], # Pass the function directly
        )
        # Await session creation
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        print("CREATED NEW SESSION:")
        print(f"\tSession ID: {SESSION_ID}")

        runner = Runner(
            agent=weather_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )

        await call_agent_async("What is the weather in London?", runner, USER_ID, SESSION_ID)
        
    except Exception as e:
        print(f"❌ Could not create or run GPT agent '{AGENT_MODEL}'. Check API Key and model name. Error: {e}")

# Run the async main
asyncio.run(main())
