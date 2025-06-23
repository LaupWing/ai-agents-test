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
        # Debug: Check what's available in the context
        print(f"🔍 DEBUG: Available artifacts: {await tool_context.list_artifacts()}")
        print(f"🔍 DEBUG: Tool context type: {type(tool_context)}")
        print(f"🔍 DEBUG: Tool context attributes: {dir(tool_context)}")
        
        # Get list of artifacts and use the first video file
        available_artifacts = await tool_context.list_artifacts()
        if not available_artifacts:
            return "No files uploaded. Please upload a workout video first!"
        
        # Find a video file (assuming common video extensions)
        video_filename = None
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        
        for artifact_name in available_artifacts:
            if any(artifact_name.lower().endswith(ext) for ext in video_extensions):
                video_filename = artifact_name
                break
        
        if not video_filename:
            return f"No video file found. Available files: {available_artifacts}"
        
        print(f"🎥 DEBUG: Using video file: {video_filename}")
        
        # Initialize Gemini client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY not found in environment"
        
        client = genai.Client(api_key=api_key)
        
        # Load video from ADK artifacts
        video_artifact = await tool_context.load_artifact(filename=video_filename)
        if not video_artifact:
            print(f"❌ DEBUG: Could not load artifact: {video_filename}")
            return f"Could not find video: {video_filename}"
        
        print(f"✅ DEBUG: Successfully loaded video artifact")
        
        # Save video temporarily for Gemini upload
        temp_video_path = f"/tmp/{video_filename}"
        with open(temp_video_path, 'wb') as f:
            f.write(video_artifact.inline_data.data)
        
        print(f"💾 DEBUG: Saved temp file: {temp_video_path}")
        
        # Upload video to Gemini
        myfile = client.files.upload(file=temp_video_path)
        print(f"⬆️ DEBUG: Uploaded to Gemini, file URI: {myfile.uri}")
        
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