import asyncio
from utils.interaction import call_agent_async
from config import APP_NAME, USER_ID, SESSION_ID
from agents.weather_agent.agent import weather_agent_team
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

async def main():
    print("\n--- Testing Agent Team Delegation ---")
    session_service = InMemorySessionService()
    session  = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    
    runner_agent_team = Runner(
        agent=weather_agent_team,
        app_name=APP_NAME,
        session_service=session_service
    )

    # --- Interactions using await (correct within async def) ---
    await call_agent_async(query = "Hello there!",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    await call_agent_async(query = "What is the weather in New York?",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    await call_agent_async(query = "Thanks, bye!",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

if __name__ == "__main__":
    asyncio.run(main())
