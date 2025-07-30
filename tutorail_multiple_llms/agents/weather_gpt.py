from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from agents.shared_tools import get_weather
from config import MODEL_GPT_4O

def build_gpt_agent():
    return Agent(
        name="weather_agent_gpt",
        model=LiteLlm(model=MODEL_GPT_4O),
        description="Weather agent using GPT-4o",
        instruction="Use get_weather to answer weather questions.",
        tools=[get_weather],
    )
