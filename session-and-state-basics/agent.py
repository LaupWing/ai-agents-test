from dotenv import load_dotenv
from google.adk.runners import Runner
from google.genai import types
from google.adk.session import InMemorySessionService

load_dotenv() 


session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """
}


# Create a NEW session
APP_NAME = "Brandon Bot"
USER_ID = "brandon_hancock"
SESSION_ID = str(uuid.uuid4())
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")