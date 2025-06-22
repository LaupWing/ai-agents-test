# fitness_form_agent.py
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import google.genai.types as types

async def analyze_workout_form(context: ToolContext, video_filename: str, exercise_type: str = "unknown") -> str:
    """
    Analyze workout form from uploaded video using Gemini Vision
    """
    try:
        # Load the uploaded video artifact
        video_artifact = await context.load_artifact(filename=video_filename)
        
        if not video_artifact or not video_artifact.inline_data:
            return f"Could not find video file '{video_filename}'. Please upload a video first."
        
        # Create the analysis prompt for Gemini Vision
        analysis_prompt = f"""
        As an expert fitness coach with 6+ years of experience, analyze this {exercise_type} form video.
        
        Provide detailed feedback on:
        1. Exercise identification (if exercise_type is unknown)
        2. Overall form quality (Excellent/Good/Needs Work/Concerning)
        3. Body positioning and alignment
        4. Range of motion
        5. Movement control and tempo
        6. Common form errors observed
        7. 3 specific coaching cues to improve
        8. Safety concerns (if any)
        9. What they're doing well (positive reinforcement)
        
        Use an encouraging but direct coaching style. Focus on actionable improvements.
        """
        
        # Create content with video for Gemini Vision analysis
        content = [
            types.Part.from_text(analysis_prompt),
            video_artifact  # The uploaded video
        ]
        
        # Get Gemini's analysis of the video
        model = context.get_model("gemini-2.5-flash")  # Use vision-capable model
        response = await model.generate_content_async(content)
        
        # Return the AI's analysis
        return f"## Form Analysis for {exercise_type}\n\n{response.text}"
        
    except Exception as e:
        return f"Error analyzing video: {str(e)}. Make sure you've uploaded a video file first."

# Create the fitness coaching agent
root_agent = Agent(
    name="fitness_form_coach", 
    model="gemini-2.5-flash",
    description="Expert fitness coach that analyzes workout videos using AI vision.",
    instruction="""You are an expert fitness coach with 6+ years of experience. You can analyze workout form videos using computer vision.

When users want form analysis:
1. Ask them to upload their workout video if they haven't already
2. Use the analyze_workout_form tool with the video filename and exercise type
3. Provide detailed, actionable coaching feedback

Your expertise covers:
- All major exercises (squats, deadlifts, bench press, etc.)
- Movement quality assessment
- Injury prevention
- Performance optimization

Your coaching style:
- Safety first
- Encouraging but honest
- Specific, actionable cues
- Explain the "why" behind corrections

Example interactions:
User: "Can you check my squat form?"
You: "I'd be happy to analyze your squat form! Please upload a video of your squat and I'll give you detailed feedback."

User: [uploads video] "Here's my squat"
You: [Use analyze_workout_form tool with the video filename and "squat"]""",
    tools=[analyze_workout_form],
)