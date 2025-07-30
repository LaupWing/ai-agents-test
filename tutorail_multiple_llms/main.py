import asyncio
from agents.weather_gpt import build_gpt_agent
from agents.weather_claude import build_claude_agent
from runners.runner_factory import build_runner
from utils.interaction import call_agent_async
from config import APP_NAME, USER_ID
from google.adk.sessions import InMemorySessionService

async def main():
    session_gpt = InMemorySessionService()
    await session_gpt.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="gpt_session"
    )
    session_claude = InMemorySessionService()
    await session_claude.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="claude_session"
    )
    


    runner_gpt = build_runner(build_gpt_agent(), session_gpt)
    runner_claude = build_runner(build_claude_agent(), session_claude)

    await call_agent_async("What's the weather in Amsterdm?", runner_gpt, USER_ID, "gpt_session")
    await call_agent_async("What's the weather in Amsterdm?", runner_claude, USER_ID, "claude_session")

if __name__ == "__main__":
    asyncio.run(main())
