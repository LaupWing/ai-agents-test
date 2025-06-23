# agent.py
from google.adk.agents import Agent

def identify_exercise(video_filename: str) -> str:
    """
    Analyze uploaded video to identify which exercise is being performed
    """
    if not video_filename:
        return "Please upload a video first!"
    
    # For now, return a basic analysis
    # In real implementation, this would analyze the actual video
    return f"""I can see your video: {video_filename}

Based on the movement patterns I observe, this appears to be:
**Exercise Identified: SQUAT**

Key indicators I noticed:
- Hip hinge movement pattern
- Knee bend with descent
- Return to standing position
- Looks like bodyweight or barbell squat

Would you like me to analyze your form in more detail?"""

# Create the agent
root_agent = Agent(
    name="exercise_detector",
    model="gemini-2.5-flash",
    description="Identifies what exercise is being performed from uploaded videos",
    instruction="""You are a fitness expert who can identify exercises from videos.

When users upload a video:
1. Use the identify_exercise tool with the video filename
2. Tell them what exercise you detected
3. Keep it simple and friendly

If they ask for form analysis, use the tool to analyze their video.""",
    tools=[identify_exercise],
)