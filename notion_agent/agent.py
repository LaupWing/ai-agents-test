# agent.py
from notion_tool import NotionDatabaseTool
from google.adk.agents import Agent
import os

notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

notion_tool = NotionDatabaseTool(notion_token=notion_token, database_id=database_id)

def fetch_and_process_posts()  -> dict:
    data = notion_tool.query_database_with_pagination()
    mapped_data = notion_tool.map_properties(data)
    return {
        "type": "notion_posts",
        "data": mapped_data
    }

root_agent = Agent(
    name="notion_post_reader",
    model="gemini-2.0-flash",
    description="Agent to read and process posts from a Notion database.",
    instruction="You are a helpful agent who can read and process posts from a Notion database.",
    tools=[fetch_and_process_posts],
)
