import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService
from question_answering_agent import question_answering_agent

load_dotenv()

# Constants
APP_NAME = "Brandon Bot"
USER_ID = "brandon_hancock"
SESSION_ID = str(uuid.uuid4())

# Initial user state
initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """
}

# Async main
async def main():
    session_service_stateful = InMemorySessionService()

    # Await session creation
    await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")

    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role="user", parts=[types.Part(text="What is Brandon's favorite TV show?")]
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final Response: {event.content.parts[0].text}")

    print("==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("==== Final Session State ====")
    for key, value in session.state.items():
        print(f"{key}: {value}")

# Run the async main
asyncio.run(main())
