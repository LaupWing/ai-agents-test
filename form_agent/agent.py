# agent.py
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google import genai
import os
import uuid

async def analyze_exercise_form(tool_context: ToolContext) -> str:
    """
    Analyze uploaded video for exercise form correction
    """
    try:
        print("🔍 DEBUG: Starting exercise form analysis...")
        print(f"🔍 DEBUG: User content: {tool_context.user_content}")
        
        # Look for video in the user content
        video_part = None
        if tool_context.user_content and tool_context.user_content.parts:
            print(f"🔍 DEBUG: Found {len(tool_context.user_content.parts)} parts in user content")
            for i, part in enumerate(tool_context.user_content.parts):
                print(f"🔍 DEBUG: Part {i}: type={type(part)}, has_inline_data={hasattr(part, 'inline_data')}")
                if hasattr(part, 'inline_data') and part.inline_data:
                    print(f"🔍 DEBUG: Part {i} mime_type: {part.inline_data.mime_type}")
                    if part.inline_data.mime_type.startswith('video/'):
                        video_part = part
                        print(f"🎥 DEBUG: Found video part at index {i}!")
                        break
                if hasattr(part, 'text'):
                    print(f"🔍 DEBUG: Part {i} text: {part.text[:50]}...")
        
        if not video_part:
            print("❌ DEBUG: No video found in user content")
            return "No video found. Please upload a clear video of your exercise for form analysis!"
        
        print(f"🎥 DEBUG: Found video with mime_type: {video_part.inline_data.mime_type}")
        print(f"🎥 DEBUG: Video data size: {len(video_part.inline_data.data)} bytes")
        
        # Save video locally so you can verify it's working
        file_extension = "mp4"
        if "quicktime" in video_part.inline_data.mime_type or "mov" in video_part.inline_data.mime_type:
            file_extension = "mov"
        elif "webm" in video_part.inline_data.mime_type:
            file_extension = "webm"
        elif "avi" in video_part.inline_data.mime_type:
            file_extension = "avi"
        
        local_filename = f"uploaded_video_{uuid.uuid4().hex[:8]}.{file_extension}"
        local_path = f"/tmp/{local_filename}"
        
        with open(local_path, 'wb') as f:
            f.write(video_part.inline_data.data)
        
        print(f"💾 DEBUG: Saved video locally to: {local_path}")
        
        # Also save to current directory so you can easily see it
        # current_dir_path = f"./{local_filename}"
        # with open(current_dir_path, 'wb') as f:
        #     f.write(video_part.inline_data.data)
        
        print(f"💾 DEBUG: ALSO saved video to current directory: {current_dir_path}")
        
        # Initialize Gemini client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ DEBUG: No GOOGLE_API_KEY found")
            return "Error: GOOGLE_API_KEY not found in environment"
        
        print("🤖 DEBUG: Initializing Gemini client...")
        client = genai.Client(api_key=api_key)
        
        # Upload video to Gemini
        print(f"⬆️ DEBUG: Uploading video to Gemini: {local_path}")
        myfile = client.files.upload(file=local_path)
        print(f"⬆️ DEBUG: Successfully uploaded! File URI: {myfile.uri}")
        
        # Wait for processing
        import time
        print("⏳ DEBUG: Waiting 8 seconds for Gemini processing...")
        time.sleep(8)
        
        # Analyze with Gemini Vision
        print("🧠 DEBUG: Sending to Gemini for form analysis...")
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[
                myfile, 
                """Analyze this exercise video for form correction. You are an expert fitness coach.

                Provide detailed feedback on:
                1. **Exercise Identification**: What exercise is being performed?
                2. **Rep Count**: How many repetitions do you see?
                3. **Form Analysis**: 
                   - Body positioning and alignment
                   - Range of motion quality
                   - Movement tempo and control
                4. **Form Issues**: Specific problems you observe
                5. **Corrections**: 3 specific coaching cues to improve form
                6. **Safety Concerns**: Any injury risks you notice
                7. **Overall Assessment**: Rate form from 1-10 and give encouraging feedback

                Be specific, actionable, and encouraging. Focus on safety first, then performance improvement."""
            ]
        )
        
        print(f"✅ DEBUG: Got response from Gemini!")
        print(f"📝 DEBUG: Response length: {len(response.text)} characters")
        
        # Clean up temp file (but keep the one in current directory)
        try:
            os.remove(local_path)
            print(f"🗑️ DEBUG: Cleaned up temp file: {local_path}")
        except:
            print(f"⚠️ DEBUG: Could not clean up temp file: {local_path}")
        
        return f"🏋️ **Exercise Form Analysis Complete!**\n\n{response.text}\n\n*Video saved as: {current_dir_path}*"
        
    except Exception as e:
        print(f"💥 DEBUG: Error occurred: {str(e)}")
        import traceback
        print(f"💥 DEBUG: Full traceback: {traceback.format_exc()}")
        return f"Error analyzing video: {str(e)}"

# Create the agent
root_agent = Agent(
    name="form_coach",
    model="gemini-2.5-flash",
    description="Analyzes exercise form from workout videos using AI vision",
    instruction="""You are an expert fitness coach who analyzes exercise form from videos.

When users upload a workout video, use the analyze_exercise_form tool to provide detailed form correction and coaching feedback.

Be encouraging, specific, and focus on safety and proper technique.""",
    tools=[analyze_exercise_form],
)