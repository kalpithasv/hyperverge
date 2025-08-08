from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import *
from app.generator import generate_assessment_from_ai, generate_demotion_assessment
from app.evaluator import evaluate_answers, analyze_skill_performance

app = FastAPI(
    title="AI Assessment System",
    description="AI-powered assessment generation and evaluation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate", response_model=AssessmentResponse)
async def generate_assessment(data: AssessmentRequest):
    """
    Generate a comprehensive assessment using AI based on role, skills, and difficulty
    """
    try:
        return generate_assessment_from_ai(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate assessment: {str(e)}")

@app.post("/evaluate", response_model=UserFeedback)
async def evaluate_assessment(submission: AssessmentSubmission):
    """
    Evaluate user answers and provide comprehensive feedback with level assessment
    """
    try:
        return evaluate_answers(submission)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate assessment: {str(e)}")

@app.post("/generate-demotion", response_model=AssessmentResponse)
async def generate_demotion_assessment_endpoint(data: AssessmentRequest):
    """
    Generate a simplified assessment for users who need to be demoted to a lower level
    """
    try:
        target_difficulty = "Beginner" if data.difficulty in ["Intermediate", "Advanced"] else "Beginner"
        return generate_demotion_assessment(data.role, data.skills, target_difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate demotion assessment: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "AI Assessment System"}

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "AI Assessment System API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate - Generate assessment",
            "evaluate": "/evaluate - Evaluate answers",
            "demotion": "/generate-demotion - Generate demotion assessment",
            "health": "/health - Health check"
        }
    }
