from google.adk.runners import Runner
from sessions.memory import create_session_service
from config import APP_NAME

def build_runner(agent, session_id):
    return Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=create_session_service()
    )
