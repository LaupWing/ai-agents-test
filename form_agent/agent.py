# fitness_form_agent.py
from google.adk.agents import Agent
import os
import base64
import requests
from datetime import datetime

# Environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def analyze_workout_form(video_file_path: str, exercise_type: str = "", user_id: str = "") -> dict:
    """
    Analyze workout form from uploaded video using Gemini Vision
    """
    try:
        # Read video file
        with open(video_file_path, 'rb') as video_file:
            video_data = video_file.read()
            video_base64 = base64.b64encode(video_data).decode()
        
        # Create detailed analysis prompt based on your coaching expertise
        analysis_prompt = f"""
        As an expert fitness coach with 6+ years of experience training clients, analyze this {exercise_type} form video.
        
        Provide a comprehensive form analysis covering:
        
        1. EXERCISE IDENTIFICATION (if not specified):
           - What exercise is being performed?
           - Exercise variation/style
        
        2. FORM ANALYSIS:
           - Body positioning and alignment
           - Range of motion quality
           - Movement pattern efficiency
           - Tempo and control
        
        3. SPECIFIC TECHNIQUE POINTS:
           - Setup and starting position
           - Movement execution
           - End position and lockout
           - Breathing pattern (if observable)
        
        4. COMMON ISSUES IDENTIFIED:
           - Form breakdowns or compensations
           - Safety concerns
           - Efficiency problems
        
        5. SPECIFIC IMPROVEMENTS:
           - 2-3 actionable coaching cues
           - Mobility/strength work recommendations
           - Progression or regression suggestions
        
        6. POSITIVE REINFORCEMENT:
           - What they're doing well
           - Improvements from previous sessions (if applicable)
        
        Use my coaching style:
        - Direct but encouraging
        - Focus on safety first
        - Give specific, actionable cues
        - Explain the "why" behind corrections
        - Use analogies that make sense
        
        Rate overall form: Excellent/Good/Needs Work/Concerning
        """
        
        # Simulate Gemini Vision API call (replace with actual implementation)
        # In real implementation, you'd use Google's Gemini API
        analysis_result = {
            "exercise_identified": exercise_type or "Squat",
            "overall_rating": "Good",
            "body_alignment": "Good knee tracking, slight forward lean",
            "range_of_motion": "Full depth achieved, good control",
            "technique_points": [
                "Setup looks solid with feet positioned well",
                "Descent controlled with good hip hinge",
                "Good depth below parallel"
            ],
            "issues_identified": [
                "Slight forward lean at bottom position",
                "Minor knee cave on ascent"
            ],
            "improvements": [
                "Focus on keeping chest up throughout movement",
                "Work on ankle mobility to reduce forward lean",
                "Strengthen glutes to prevent knee cave"
            ],
            "positive_feedback": [
                "Excellent depth consistency",
                "Good control on descent",
                "Strong lockout position"
            ],
            "coaching_cues": [
                "Imagine pushing the floor apart with your feet",
                "Drive through your heels on the way up",
                "Keep your chest proud throughout"
            ]
        }
        
        # Save analysis to user's profile (in-memory for now)
        # save_analysis_to_profile(user_id, analysis_result, video_file_path)
        
        return {
            "success": True,
            "analysis": analysis_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }

def get_user_form_progress(user_id: str, exercise_type: str = "") -> dict:
    """
    Get user's form progression over time (simulated data for testing)
    """
    # Simulated response - in production you'd query your database
    return {
        "user_id": user_id,
        "exercise": exercise_type,
        "total_sessions": 8,
        "improvement_trend": "Improving",
        "recent_analyses": [
            {
                "date": "2025-06-15",
                "rating": "Good",
                "key_improvement": "Better depth consistency"
            },
            {
                "date": "2025-06-10", 
                "rating": "Needs Work",
                "key_improvement": "Reduced forward lean"
            }
        ],
        "persistent_issues": ["Ankle mobility"],
        "strengths": ["Consistent depth", "Good control"]
    }

def save_analysis_to_profile(user_id: str, analysis: dict, video_path: str):
    """
    Save form analysis to user's profile for progress tracking
    (Currently just prints - replace with actual storage later)
    """
    print(f"Saving analysis for user {user_id}:")
    print(f"- Exercise: {analysis.get('exercise_identified', 'Unknown')}")
    print(f"- Rating: {analysis.get('overall_rating', 'N/A')}")
    print(f"- Video: {video_path}")
    # In production: save to database, Firebase, or file system

def generate_exercise_program(user_id: str, focus_areas: str) -> dict:
    """
    Generate targeted exercises based on form analysis weaknesses
    focus_areas should be comma-separated string like "ankle_mobility,glute_strength"
    """
    # Convert comma-separated string to list
    focus_list = [area.strip() for area in focus_areas.split(",")]
    
    # Based on identified issues, recommend specific exercises
    exercise_recommendations = {
        "ankle_mobility": [
            "Ankle wall stretches - 3x30 seconds",
            "Calf raises on elevated surface - 3x15",
            "Deep squat holds - 3x30 seconds"
        ],
        "glute_strength": [
            "Glute bridges - 3x15",
            "Clamshells - 3x12 each side", 
            "Single leg deadlifts - 3x8 each side"
        ],
        "core_stability": [
            "Plank holds - 3x30 seconds",
            "Dead bugs - 3x10 each side",
            "Bird dogs - 3x8 each side"
        ]
    }
    
    return {
        "focus_areas": focus_list,
        "recommended_exercises": exercise_recommendations,
        "frequency": "3-4x per week",
        "progression_note": "Master bodyweight versions before adding load"
    }

# Create the main fitness coaching agent and export as root_agent
root_agent = Agent(
    name="ai_fitness_coach",
    model="gemini-2.5-flash",  # Best for video analysis
    description="Expert AI fitness coach specializing in form analysis, nutrition guidance, and motivation coaching.",
    instruction="""You are an expert fitness coach with 6+ years of experience training clients. Your expertise includes:

FORM ANALYSIS:
- Video analysis of all major exercises (squats, deadlifts, bench press, etc.)
- Identifying movement compensations and safety issues
- Providing specific, actionable coaching cues
- Tracking progress over time

COACHING STYLE:
- Safety first approach
- Encouraging but direct feedback
- Focus on movement quality over quantity
- Explain the "why" behind recommendations
- Use simple analogies and cues

SPECIALIZATIONS:
- Strength training fundamentals
- Movement pattern correction
- Injury prevention
- Progressive overload principles
- Sustainable habit building

IMPORTANT - When to use tools:
1. If a user uploads a video or mentions form analysis, ALWAYS use analyze_workout_form tool
2. If asked about progress or improvement over time, use get_user_form_progress tool  
3. If form issues are identified, use generate_exercise_program tool to recommend corrective exercises

When analyzing form:
1. Always start with positive observations
2. Identify 2-3 key areas for improvement
3. Provide specific coaching cues
4. Recommend corrective exercises if needed
5. Reference previous analyses to show progress

For video analysis: When you receive video input, immediately use the analyze_workout_form function with appropriate parameters. If no video file path is provided, ask the user to upload their form video.

Remember: You're not just analyzing movement - you're coaching a real person toward their fitness goals with patience, expertise, and encouragement.""",
    tools=[analyze_workout_form, get_user_form_progress, generate_exercise_program],
)

# Example usage
if __name__ == "__main__":
    # Simulate user interaction
    print("AI Fitness Coach initialized!")
    print("Upload a form video and I'll analyze it using proven coaching methods.")
    
    # Example analysis (you'd integrate this with your app's video upload)
    # result = analyze_workout_form("user_squat_video.mp4", "squat", "user123")
    # print(result)