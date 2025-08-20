import asyncio
from utils.interaction import call_agent_async
from config import APP_NAME, USER_ID, SESSION_ID
from agents.weather_agent.agent import weather_agent_team
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

initial_state = {
    "user_preference_temperature_unit": "Celsius"
}


async def main():
    print("\n--- Testing Agent Team Delegation ---")
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    
    runner_agent_team = Runner(
        agent=weather_agent_team,
        app_name=APP_NAME,
        session_service=session_service
    )
    print("\n--- Testing State: Temp Unit Conversion & output_key ---")

    # 1. Check weather (Uses initial state: Celsius)
    print("--- Turn 1: Requesting weather in London (expect Celsius) ---")
    await call_agent_async(query= "What's the weather in London?",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # 2. Manually update state preference to Fahrenheit - DIRECTLY MODIFY STORAGE
    print("\n--- Manually Updating State: Setting unit to Fahrenheit ---")
    try:
        stored_session = session_service.sessions[APP_NAME][USER_ID][SESSION_ID]
        stored_session.state["user_preference_temperature_unit"] = "Fahrenheit"
        
        print(f"--- Stored session state updated. Current 'user_preference_temperature_unit': {stored_session.state.get('user_preference_temperature_unit', 'Not Set')} ---") # Added .get for safety
    except KeyError:
        print(f"--- Error: Could not retrieve session '{SESSION_ID}' from internal storage for user '{USER_ID}' in app '{APP_NAME}' to update state. Check IDs and if session was created. ---")
    except Exception as e:
            print(f"--- Error updating internal session state: {e} ---")

    print("\n--- Turn 2: Requesting weather in New York (expect Fahrenheit) ---")
    await call_agent_async(query= "Tell me the weather in New York.",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print("\n--- Turn 3: Sending a greeting ---")
    await call_agent_async(query= "Hi!",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

if __name__ == "__main__":
    asyncio.run(main())
