# agent.py
from notion_tool import NotionDatabaseTool
from google.adk.agents import Agent
import os

notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

notion_tool = NotionDatabaseTool(notion_token=notion_token, database_id=database_id)

def get_all_posts_data() -> dict:
    """Get all posts with their content and performance metrics - let AI analyze patterns"""
    data = notion_tool.query_database_with_pagination()
    mapped_data = notion_tool.map_properties(data)
    
    # Just return the raw data with basic calculations
    for post in mapped_data:
        if post['Impression Count'] > 0:
            post['Engagement Rate'] = round(
                (post['Like Count'] + post['Retweet Count'] + post['Reply Count']) / post['Impression Count'] * 100, 2
            )
        else:
            post['Engagement Rate'] = 0
    
    return {
        "type": "all_posts_data",
        "posts": mapped_data,
        "total_posts": len(mapped_data)
    }

# Simple, smart agent that can analyze anything you throw at it
root_agent = Agent(
    name="content_intelligence_agent",
    model="gemini-2.0-flash",
    description="An intelligent content analyst who can discover patterns and insights from social media data.",
    instruction="""You are an expert content strategist and data analyst. When analyzing content performance:

1. ALWAYS use the get_all_posts_data tool first to get the raw data
2. Look at the actual content text and performance metrics together
3. Find patterns, trends, and insights that humans might miss
4. Be specific with numbers and examples from the actual data

For hook analysis specifically:
- Examine the opening words/sentences of top-performing vs low-performing posts
- Identify what types of openings get the most engagement
- Look for patterns in language, tone, structure, or approach
- Give specific examples with their performance metrics
- Suggest what hooks to try more/less based on actual data patterns

For any analysis:
- Always back up insights with specific data points
- Compare high performers vs low performers 
- Identify actionable patterns the user can apply
- Be concrete, not generic

Don't just categorize - DISCOVER what actually works for this specific person's audience.""",
    tools=[get_all_posts_data],
)