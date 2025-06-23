import os
import logging
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool, ToolContext
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService, GcsArtifactService
from google.adk.sessions import InMemorySessionService
import google.genai as genai
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini Vision
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

async def analyze_fitness_form(video_data: Dict[str, Any], tool_context: ToolContext) -> Dict[str, Any]:
    """Analyze fitness form using Gemini Vision."""
    try:
        logger.info(f"Analyzing fitness video: {video_data}")
        
        # Load video from artifacts
        video_filename = video_data.get('video')
        if not video_filename:
            return {"error": "No video filename provided"}
            
        video_part = await tool_context.load_artifact(filename=video_filename)
        if not video_part:
            return {"error": f"Could not load video: {video_filename}"}
        
        # Initialize Gemini model for video analysis
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Structured analysis prompt for fitness
        analysis_prompt = """
        Analyze this exercise video and provide detailed form feedback in JSON format:
        {
          "exercise_name": "string",
          "total_reps": number,
          "rep_timing": ["timestamp array"],
          "form_score": number (1-10 scale),
          "form_critique": "detailed biomechanical analysis",
          "safety_concerns": ["list of safety issues"],
          "recommendations": ["specific improvement suggestions"],
          "key_muscles": ["primary muscles worked"],
          "common_mistakes": ["mistakes observed in video"]
        }
        
        Focus on:
        - Proper biomechanics and joint alignment
        - Range of motion completeness
        - Movement tempo and control
        - Potential injury risks
        - Specific corrections needed
        """
        
        # Generate analysis using Gemini Vision
        response = model.generate_content([
            video_part,
            analysis_prompt
        ])
        
        # Parse and structure response
        analysis_text = response.text
        
        # Save analysis as artifact for future reference
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        analysis_filename = f"form_analysis_{timestamp}.json"
        
        from google.genai.types import Part
        analysis_part = Part.from_text(analysis_text)
        tool_context.save_artifact(analysis_filename, analysis_part)
        
        return {
            "status": "success",
            "analysis": analysis_text,
            "analysis_file": analysis_filename,
            "video_processed": video_filename
        }
        
    except Exception as e:
        logger.error(f"Form analysis failed: {str(e)}")
        return {"error": f"Analysis failed: {str(e)}"}

def create_complete_fitness_system():
    """Create complete ADK system for fitness form analysis."""
    
    # Initialize services
    artifact_service = GcsArtifactService()  # Use GCS for production
    session_service = InMemorySessionService()
    
    # Create specialized fitness form analyzer
    fitness_agent = LlmAgent(
        name="fitness_form_expert",
        model="gemini-2.5-flash",
        description="Professional fitness form analysis using Gemini Vision",
        instruction="""
        You are an expert fitness coach specializing in biomechanical analysis.
        
        When users upload workout videos:
        1. Use analyze_fitness_form tool to process videos with Gemini Vision
        2. Provide comprehensive form feedback covering technique, safety, and improvements
        3. Count repetitions accurately with timing analysis
        4. Identify muscle activation patterns and movement quality
        5. Offer personalized recommendations based on observed form issues
        
        Always prioritize safety and proper biomechanics in your analysis.
        """,
        tools=[
            FunctionTool(analyze_fitness_form),
            FunctionTool(check_available_videos),
            FunctionTool(save_processed_video)
        ]
    )
    
    # Initialize runner with video processing capabilities
    runner = Runner(
        agent=fitness_agent,
        app_name="fitness_form_analyzer",
        session_service=session_service,
        artifact_service=artifact_service
    )
    
    return runner

# Production deployment setup
if __name__ == "__main__":
    # Create the fitness analysis system
    fitness_runner = create_complete_fitness_system()
    
    # Run the web interface for video uploads
    fitness_runner.run_web_ui()  # Access at http://localhost:8000