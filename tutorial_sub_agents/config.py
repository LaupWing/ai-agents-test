import os
from dotenv import load_dotenv
load_dotenv()

# Set your API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

APP_NAME = "weather_bot_adk"
USER_ID = "user_123"

# Model constants
MODEL_GPT_4O = "openai/gpt-4o"
MODEL_CLAUDE_SONNET = "anthropic/claude-sonnet-4-20250514"
