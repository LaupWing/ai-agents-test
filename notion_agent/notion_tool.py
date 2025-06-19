# notion_tool.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class NotionDatabaseTool:
    def __init__(self, notion_token, database_id):
        self.notion_token = notion_token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28"
        }

    def query_database_with_pagination(self):
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        all_results = []
        has_more = True
        start_cursor = None

        while has_more:
            payload = {}
            if start_cursor:
                payload["start_cursor"] = start_cursor

            response = requests.post(url, headers=self.headers, json=payload)
            data = response.json()

            all_results.extend(data.get('results', []))
            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor', None)

        return all_results

    def map_properties(self, data):
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

        sorted_data = sorted(mapped_data, key=lambda x: x['Impression Count'], reverse=True)
        return sorted_data
