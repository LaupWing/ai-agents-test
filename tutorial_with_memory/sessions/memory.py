# agents/session/init_state.py

from google.adk.sessions import InMemorySessionService

from config import APP_NAME

async def setup_stateful_session():
    session_service = InMemorySessionService()

    session_id = "session_state_demo_001"
    user_id = "user_state_demo"

    initial_state = {
        "user_preference_temperature_unit": "Celsius"
    }

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state=initial_state
    )

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    print("\n--- Initial Session State ---")
    print(session.state if session else "❌ Could not retrieve session.")

    return session_service
