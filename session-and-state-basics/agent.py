from dotenv import load_dotenv
from google.adk.runners import Runner
from google.genai import types
from google.adk.session import InMemorySessionService

load_dotenv() 


session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "John Doe",
    "user_preferences": """
    
    """
}