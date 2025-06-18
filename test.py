import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class NotionDatabaseTool:
    def __init__(self, notion_token, database_id):
        self.notion_token = notion_token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28"
        }

    def query_database_with_pagination(self, filter=None):
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        all_results = []
        has_more = True
        start_cursor = None

        while has_more:
            payload = {"filter": filter} if filter else {}
            if start_cursor:
                payload["start_cursor"] = start_cursor

            response = requests.post(url, headers=self.headers, json=payload)
            data = response.json()

            all_results.extend(data.get('results', []))
            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor', None)

        return all_results

    def map_properties(self, data):
        """Map the Notion database properties to a simpler format."""
        mapped_data = []
        
        for result in data:
            properties = result.get('properties', {})
            mapped_item = {
                "Name": properties.get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                "Tweet ID": properties.get("tweet_id", {}).get("number", None),
                "URL": properties.get("url", {}).get("url", ""),
                "Reply Count": properties.get("reply_count", {}).get("number", 0),
                "Retweet Count": properties.get("retweet_count", {}).get("number", 0),
                "Bookmark Count": properties.get("bookmark_count", {}).get("number", 0),
                "Impression Count": properties.get("impression_count", {}).get("number", 0),
                "Like Count": properties.get("like_count", {}).get("number", 0),
                "Created At": properties.get("created_at", {}).get("date", {}).get("start", ""),
                "Is Thread Head": properties.get("is_thread_head", {}).get("checkbox", False),
                "Is Thread Part": properties.get("is_thread_part", {}).get("checkbox", False),
                "Is Note Tweet": properties.get("is_note_tweet", {}).get("checkbox", False),
            }
            mapped_data.append(mapped_item)
        
        # Sort by 'Impression Count' in descending order
        sorted_data = sorted(mapped_data, key=lambda x: x['Impression Count'], reverse=True)
        
        return sorted_data


# Usage Example:
# Load the Notion token and Database ID from the .env file
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

# Check if the environment variables are loaded correctly
if not notion_token or not database_id:
    raise ValueError("Missing Notion token or database ID. Please check your .env file.")

# Initialize the NotionDatabaseTool with the token and database ID
notion_tool = NotionDatabaseTool(notion_token=notion_token, database_id=database_id)

# Query the database with pagination
data = notion_tool.query_database_with_pagination()  # Pass filter if needed
mapped_data = notion_tool.map_properties(data)

# Write the mapped data to a JSON file
output_file = "notion_data.json"
with open(output_file, "w") as f:
    # Include the count of the records in the JSON file
    json_data = {
        "record_count": len(mapped_data),
        "data": mapped_data
    }
    # Pretty print the JSON with indentation
    json.dump(json_data, f, indent=4)

# Print confirmation and record count
print(f"Data has been written to {output_file}. Total records: {len(mapped_data)}")
