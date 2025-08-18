from google.genai import types

async def call_agent_async(query, runner, user_id, session_id):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"\nUser: {query}")
            print(f"Agent: {event.content.parts[0].text}")
            break
