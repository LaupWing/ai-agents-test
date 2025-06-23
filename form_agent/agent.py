# agent.py
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google import genai
import os

async def analyze_exercise_video(tool_context: ToolContext) -> str:
    """
    Analyze uploaded video to identify exercise using real Gemini Vision
    """
    try:
        # Debug: Check user content for video
        print(f"🔍 DEBUG: User content: {tool_context.user_content}")
        
        # Look for video in the user content
        video_part = None
        if tool_context.user_content and tool_context.user_content.parts:
            for part in tool_context.user_content.parts:
                print(f"🔍 DEBUG: Part type: {type(part)}, has inline_data: {hasattr(part, 'inline_data')}")
                if hasattr(part, 'inline_data') and part.inline_data:
                    print(f"🔍 DEBUG: Found inline data with mime_type: {part.inline_data.mime_type}")
                    if part.inline_data.mime_type.startswith('video/'):
                        video_part = part
                        break
        
        if not video_part:
            return "No video found in your message. Please upload a workout video!"
        
        print(f"🎥 DEBUG: Found video with mime_type: {video_part.inline_data.mime_type}")
        
        # Initialize Gemini client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY not found in environment"
        
        client = genai.Client(api_key=api_key)
        
        # Save video temporarily for Gemini upload
        temp_video_path = f"/tmp/workout_video.mov"
        with open(temp_video_path, 'wb') as f:
            f.write(video_part.inline_data.data)
        
        print(f"💾 DEBUG: Saved temp file: {temp_video_path}")
        
        # Upload video to Gemini
        myfile = client.files.upload(file=temp_video_path)
        print(f"⬆️ DEBUG: Uploaded to Gemini, file URI: {myfile.uri}")
        
        # Wait for file to be ready (Gemini needs processing time)
        import time
        print(f"⏳ DEBUG: Waiting 8 seconds for file to be ready...")
        time.sleep(8)  # Wait 8 seconds for processing
        
        # Analyze with Gemini Vision
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[
                myfile, 
                """Analyze this exercise video and tell me:
                1. What exercise is being performed?
                2. How many reps do you count?
                3. Basic form assessment (good/needs work)
                4. One key improvement tip
                
                Keep it simple and encouraging!"""
            ]
        )
        
        print(f"🤖 DEBUG: Got response from Gemini")
        
        # Clean up temp file
        os.remove(temp_video_path)
        print(f"🗑️ DEBUG: Cleaned up temp file")
        
        return response.text
        
    except Exception as e:
        print(f"💥 DEBUG: Error occurred: {str(e)}")
        return f"Error analyzing video: {str(e)}"

# Create the agent
root_agent = Agent(
    name="exercise_detector",
    model="gemini-2.5-flash",
    description="Analyzes exercise videos using Gemini Vision",
    instruction="""You are a friendly fitness coach who analyzes workout videos.

When users upload a video, use the analyze_exercise_video tool to get real AI analysis of their form and technique.

Be encouraging and helpful!""",
    tools=[analyze_exercise_video],
)