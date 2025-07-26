import os
import asyncio
import logging
import warnings
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types 

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")