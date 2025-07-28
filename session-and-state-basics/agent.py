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
