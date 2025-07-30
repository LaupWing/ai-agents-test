from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from agents.shared_tools import get_weather
from config import MODEL_CLAUDE_SONNET

def build_claude_agent():
    return Agent(
        name="weather_agent_claude",
        model=LiteLlm(model=MODEL_CLAUDE_SONNET),
        description="Weather agent using Claude Sonnet",
        instruction="Use get_weather to answer weather questions.",
        tools=[get_weather],
    )
