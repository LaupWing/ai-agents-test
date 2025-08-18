import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

APP_NAME = "weather_tutorial_agent_team"
USER_ID = "user_1_agent_team"
SESSION_ID = "session_001_agent_team"

MODEL_GPT_4O = "openai/gpt-4o"
MODEL_CLAUDE_SONNET = "anthropic/claude-sonnet-4-20250514"
