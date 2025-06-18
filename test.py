import requests

class NotionDatabaseTool:
    def __init__(self, notion_token, database_id):
        self.notion_token = notion_token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28"
        }

    def query_database(self, filter=None):
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        payload = {"filter": filter} if filter else {}
        response = requests.post(url, headers=self.headers, json=payload)
        
        # If successful, return the JSON response.
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error querying Notion database: {response.status_code}, {response.text}")

    def map_properties(self, data):
        """Map the Notion database properties to a simpler format."""
        mapped_data = []
        
        for result in data.get('results', []):
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
        
        return mapped_data

# Usage Example:
notion_token = "your_notion_token"
database_id = "your_database_id"

notion_tool = NotionDatabaseTool(notion_token=notion_token, database_id=database_id)

# Query the database and map the properties
data = notion_tool.query_database()  # Pass filter if needed
mapped_data = notion_tool.map_properties(data)

# Print the mapped data (list of dictionaries)
for item in mapped_data:
    print(item)
