# agent.py
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google import genai
import os

def analyze_exercise_video(video_filename: str, tool_context: ToolContext) -> str:
    """
    Analyze uploaded video to identify exercise using real Gemini Vision
    """
    try:
        # Initialize Gemini client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY not found in environment"
        
        client = genai.Client(api_key=api_key)
        print(video_filename)
        # Load video from ADK artifacts
        video_artifact = tool_context.load_artifact(filename=video_filename)
        if not video_artifact:
            return f"Could not find video: {video_filename}"
        
        # Save video temporarily for Gemini upload
        temp_video_path = f"/tmp/{video_filename}"
        with open(temp_video_path, 'wb') as f:
            f.write(video_artifact.inline_data.data)
        
        # Upload video to Gemini
        myfile = client.files.upload(file=temp_video_path)
        
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
        
        # Clean up temp file
        os.remove(temp_video_path)
        
        return response.text
        
    except Exception as e:
        print(f"Error analyzing video: {str(e)}")
        return f"Error analyzing video: {str(e)}"

# Create the agent
root_agent = Agent(
    name="exercise_detector",
    model="gemini-2.5-flash",
    description="Analyzes exercise videos using Gemini Vision",
    instruction="""You are a arrogant fitness coach who analyzes workout videos.

When users upload a video, use the analyze_exercise_video tool to get real AI analysis of their form and technique.

Be encouraging and helpful!""",
    tools=[analyze_exercise_video],
)