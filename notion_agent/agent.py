# agent.py
from notion_tool import NotionDatabaseTool
from google.adk.agents import Agent
import os

notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

notion_tool = NotionDatabaseTool(notion_token=notion_token, database_id=database_id)

def fetch_and_analyze_posts() -> dict:
    """Fetch posts and return structured data for analysis"""
    data = notion_tool.query_database_with_pagination()
    mapped_data = notion_tool.map_properties(data)
    
    # Calculate some basic metrics for the agent to work with
    total_posts = len(mapped_data)
    total_impressions = sum(post['Impression Count'] for post in mapped_data)
    total_likes = sum(post['Like Count'] for post in mapped_data)
    total_retweets = sum(post['Retweet Count'] for post in mapped_data)
    
    # Get top and bottom performers
    top_posts = mapped_data[:5]  # Already sorted by impressions
    bottom_posts = mapped_data[-5:] if len(mapped_data) >= 5 else []
    
    # Calculate engagement rates
    posts_with_engagement = []
    for post in mapped_data:
        if post['Impression Count'] > 0:
            engagement_rate = (post['Like Count'] + post['Retweet Count'] + post['Reply Count']) / post['Impression Count'] * 100
            post['Engagement Rate'] = round(engagement_rate, 2)
            posts_with_engagement.append(post)
    
    return {
        "type": "notion_posts_analysis",
        "summary_stats": {
            "total_posts": total_posts,
            "total_impressions": total_impressions,
            "total_likes": total_likes,
            "total_retweets": total_retweets,
            "average_impressions": round(total_impressions / total_posts if total_posts > 0 else 0),
            "average_likes": round(total_likes / total_posts if total_posts > 0 else 0)
        },
        "top_performing_posts": top_posts,
        "bottom_performing_posts": bottom_posts,
        "posts_with_engagement_rates": posts_with_engagement
    }

def get_content_type_analysis() -> dict:
    """Analyze performance by content type"""
    data = notion_tool.query_database_with_pagination()
    mapped_data = notion_tool.map_properties(data)
    
    thread_heads = [post for post in mapped_data if post['Is Thread Head']]
    thread_parts = [post for post in mapped_data if post['Is Thread Part']]
    note_tweets = [post for post in mapped_data if post['Is Note Tweet']]
    regular_tweets = [post for post in mapped_data if not post['Is Thread Head'] and not post['Is Thread Part'] and not post['Is Note Tweet']]
    
    def analyze_group(posts, group_name):
        if not posts:
            return {"group": group_name, "count": 0}
        
        total_impressions = sum(post['Impression Count'] for post in posts)
        total_engagement = sum(post['Like Count'] + post['Retweet Count'] + post['Reply Count'] for post in posts)
        avg_impressions = total_impressions / len(posts)
        avg_engagement = total_engagement / len(posts)
        
        return {
            "group": group_name,
            "count": len(posts),
            "avg_impressions": round(avg_impressions),
            "avg_engagement": round(avg_engagement),
            "total_impressions": total_impressions
        }
    
    return {
        "type": "content_type_analysis",
        "thread_heads": analyze_group(thread_heads, "Thread Heads"),
        "thread_parts": analyze_group(thread_parts, "Thread Parts"), 
        "note_tweets": analyze_group(note_tweets, "Note Tweets"),
        "regular_tweets": analyze_group(regular_tweets, "Regular Tweets")
    }

# Create an intelligent agent that can actually analyze and make observations
root_agent = Agent(
    name="social_media_analyst",
    model="gemini-2.0-flash",
    description="An intelligent social media analyst who can analyze post performance and provide strategic insights.",
    instruction="""You are an expert social media analyst. When someone asks you about their content performance, you should:

1. USE THE TOOLS to get the data first
2. ANALYZE the data thoroughly - look for patterns, trends, and insights
3. PROVIDE SPECIFIC OBSERVATIONS with numbers to back them up
4. GIVE ACTIONABLE RECOMMENDATIONS based on what the data shows

Key things to analyze:
- Which content types perform best (threads vs regular tweets vs note tweets)
- Engagement rate patterns (likes + retweets + replies / impressions)
- Top performing content themes or characteristics
- Content frequency vs performance correlation
- Best and worst performing posts with reasons why

Always be specific with your insights. Instead of saying "some posts do well", say "Your thread heads average 2,300 impressions compared to 890 for regular tweets, suggesting your audience prefers longer-form content."

Be data-driven, insightful, and actionable in your analysis.""",
    tools=[fetch_and_analyze_posts, get_content_type_analysis],
)