from google.adk.runners import Runner
from config import APP_NAME

def build_runner(agent, session_service):
    return Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service
    )
