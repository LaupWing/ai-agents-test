# agent.py
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google import genai
import os
import uuid

async def analyze_body_fat(tool_context: ToolContext) -> str:
    """
    Analyze uploaded image to estimate body fat percentage
    """
    try:
        print("🔍 DEBUG: Starting body fat analysis...")
        print(f"🔍 DEBUG: User content: {tool_context.user_content}")
        
        # Look for image in the user content
        image_part = None
        if tool_context.user_content and tool_context.user_content.parts:
            print(f"🔍 DEBUG: Found {len(tool_context.user_content.parts)} parts in user content")
            for i, part in enumerate(tool_context.user_content.parts):
                print(f"🔍 DEBUG: Part {i}: type={type(part)}, has_inline_data={hasattr(part, 'inline_data')}")
                if hasattr(part, 'inline_data') and part.inline_data:
                    print(f"🔍 DEBUG: Part {i} mime_type: {part.inline_data.mime_type}")
                    if part.inline_data.mime_type.startswith('image/'):
                        image_part = part
                        print(f"📸 DEBUG: Found image part at index {i}!")
                        break
                if hasattr(part, 'text'):
                    print(f"🔍 DEBUG: Part {i} text: {part.text[:50]}...")
        
        if not image_part:
            print("❌ DEBUG: No image found in user content")
            return "No image found. Please upload a clear photo showing your physique for body fat analysis!"
        
        print(f"📸 DEBUG: Found image with mime_type: {image_part.inline_data.mime_type}")
        print(f"📸 DEBUG: Image data size: {len(image_part.inline_data.data)} bytes")
        
        # Save image locally so you can verify it's working
        file_extension = "jpg"
        if "png" in image_part.inline_data.mime_type:
            file_extension = "png"
        elif "gif" in image_part.inline_data.mime_type:
            file_extension = "gif"
        
        local_filename = f"uploaded_image_{uuid.uuid4().hex[:8]}.{file_extension}"
        local_path = f"/tmp/{local_filename}"
        
        with open(local_path, 'wb') as f:
            f.write(image_part.inline_data.data)
        
        print(f"💾 DEBUG: Saved image locally to: {local_path}")
        
        # Also save to current directory so you can easily see it
        current_dir_path = f"./{local_filename}"
        with open(current_dir_path, 'wb') as f:
            f.write(image_part.inline_data.data)
        
        print(f"💾 DEBUG: ALSO saved image to current directory: {current_dir_path}")
        
        # Initialize Gemini client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ DEBUG: No GOOGLE_API_KEY found")
            return "Error: GOOGLE_API_KEY not found in environment"
        
        print("🤖 DEBUG: Initializing Gemini client...")
        client = genai.Client(api_key=api_key)
        
        # Upload image to Gemini
        print(f"⬆️ DEBUG: Uploading image to Gemini: {local_path}")
        myfile = client.files.upload(file=local_path)
        print(f"⬆️ DEBUG: Successfully uploaded! File URI: {myfile.uri}")
        
        # Wait a bit for processing
        import time
        print("⏳ DEBUG: Waiting 3 seconds for Gemini processing...")
        time.sleep(3)
        
        # Analyze with Gemini Vision
        print("🧠 DEBUG: Sending to Gemini for analysis...")
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[
                myfile, 
                """Look at this person's physique and estimate their body fat percentage.

                Provide:
                1. Estimated body fat percentage range (e.g., "15-18%")
                2. Body composition category (lean, average, above average, etc.)
                3. Visible muscle definition level
                4. Key visual indicators you used for the estimate
                5. General fitness observations

                Be professional and encouraging. Remember this is an estimate based on visual appearance only."""
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
        
        return f"🏋️ **Body Fat Analysis Complete!**\n\n{response.text}\n\n*Image saved as: {current_dir_path}*"
        
    except Exception as e:
        print(f"💥 DEBUG: Error occurred: {str(e)}")
        import traceback
        print(f"💥 DEBUG: Full traceback: {traceback.format_exc()}")
        return f"Error analyzing image: {str(e)}"

# Create the agent
root_agent = Agent(
    name="body_fat_analyzer",
    model="gemini-2.5-flash",
    description="Analyzes body composition from photos using AI vision",
    instruction="""You are a friendly fitness assessment expert who can estimate body fat percentage from photos.

When users upload a photo of themselves, use the analyze_body_fat tool to get AI analysis of their body composition.

Be professional, encouraging, and remind them that this is an estimate for general guidance only.""",
    tools=[analyze_body_fat],
)