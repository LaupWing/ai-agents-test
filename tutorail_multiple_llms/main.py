import asyncio
from agents.weather_gpt import build_gpt_agent
from agents.weather_claude import build_claude_agent
from sessions.memory import create_session_service
from runners.runner_factory import build_runner
from utils.interaction import call_agent_async
from config import APP_NAME, USER_ID

async def main():
    session_gpt = await create_session_service().create_session(APP_NAME, USER_ID, "gpt_session")
    session_claude = await create_session_service().create_session(APP_NAME, USER_ID, "claude_session")

    runner_gpt = build_runner(build_gpt_agent(), "gpt_session")
    runner_claude = build_runner(build_claude_agent(), "claude_session")

    await call_agent_async("What's the weather in Tokyo?", runner_gpt, USER_ID, "gpt_session")
    await call_agent_async("What's the weather in London?", runner_claude, USER_ID, "claude_session")

if __name__ == "__main__":
    asyncio.run(main())
