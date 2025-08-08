from app.schemas import AssessmentSubmission, UserFeedback, SkillAnalysis
from app.openai_client import chat_with_openai, parse_json_response
from app.generator import generate_demotion_assessment
import json

def evaluate_answers(submission: AssessmentSubmission) -> UserFeedback:
    """
    Evaluate user answers using AI and provide comprehensive feedback
    """
    
    # Create detailed evaluation prompt
    prompt = f"""
    You are an expert assessment evaluator. Analyze the following user responses and provide comprehensive feedback.

    ASSESSMENT DETAILS:
    - Role: {submission.role}
    - Skills Tested: {', '.join(submission.skills)}
    - Difficulty Level: {submission.difficulty}
    - Total Questions: {len(submission.responses)}

    USER RESPONSES:
    {json.dumps([{
        'question': response.question,
        'user_answer': response.user_answer,
        'question_type': response.question_type,
        'skill': response.skill,
        'difficulty': response.difficulty
    } for response in submission.responses], indent=2)}

    EVALUATION REQUIREMENTS:
    1. Score each answer (0-100 points total)
    2. Analyze performance by skill area
    3. Determine actual competency level (Beginner/Intermediate/Advanced)
    4. Identify weak areas and provide specific recommendations
    5. Assess if user should be demoted to a lower level
    6. Provide actionable feedback

    SCORING GUIDELINES:
    - MCQs: 1 point each (15 total)
    - SAQs: 2 points each (10 total) 
    - Case Study: 5 points (5 total)
    - Total possible: 30 points

    LEVEL DETERMINATION:
    - Beginner: 0-15 points (0-50%)
    - Intermediate: 16-24 points (51-80%)
    - Advanced: 25-30 points (81-100%)

    DEMOTION CRITERIA:
    - If user scored <40% on Intermediate level, suggest Beginner
    - If user scored <60% on Advanced level, suggest Intermediate
    - Consider skill-specific weaknesses

    RESPONSE FORMAT (JSON):
    {{
        "score": 18,
        "actual_level": "Intermediate",
        "message": "Detailed feedback message",
        "skill_breakdown": {{
            "SQL": {{
                "score": 8,
                "total_possible": 10,
                "percentage": 80,
                "level": "Intermediate",
                "weak_areas": ["Complex joins", "Window functions"],
                "recommendations": ["Practice advanced SQL concepts"]
            }}
        }},
        "recommendations": [
            "Focus on data analysis fundamentals",
            "Practice SQL optimization techniques"
        ],
        "should_demote": false,
        "suggested_assessment": null
    }}

    Provide honest, constructive feedback that helps the user improve.
    """
    
    try:
        # Get AI evaluation
        raw_response = chat_with_openai(prompt, temperature=0.2)
        evaluation_data = parse_json_response(raw_response)
        
        # Determine if demotion is needed
        should_demote = evaluation_data.get("should_demote", False)
        suggested_assessment = None
        
        if should_demote:
            # Generate demotion assessment
            target_difficulty = "Beginner" if submission.difficulty in ["Intermediate", "Advanced"] else "Beginner"
            demotion_assessment = generate_demotion_assessment(
                submission.role, 
                submission.skills, 
                target_difficulty
            )
            suggested_assessment = f"Beginner assessment for {submission.role}"
        
        return UserFeedback(
            score=evaluation_data.get("score", 0),
            actual_level=evaluation_data.get("actual_level", "Beginner"),
            message=evaluation_data.get("message", "Assessment completed."),
            skill_breakdown=evaluation_data.get("skill_breakdown", {}),
            recommendations=evaluation_data.get("recommendations", []),
            should_demote=should_demote,
            suggested_assessment=suggested_assessment
        )
        
    except Exception as e:
        raise ValueError(f"Failed to evaluate assessment: {str(e)}")

def analyze_skill_performance(responses: list, skill: str) -> SkillAnalysis:
    """
    Analyze performance for a specific skill area
    """
    
    skill_responses = [r for r in responses if r.skill == skill]
    
    if not skill_responses:
        return SkillAnalysis(
            skill=skill,
            score=0,
            level="Not Tested",
            weak_areas=[],
            recommendations=[]
        )
    
    prompt = f"""
    Analyze the user's performance in {skill} based on these responses:
    
    {json.dumps([{
        'question': response.question,
        'user_answer': response.user_answer,
        'question_type': response.question_type
    } for response in skill_responses], indent=2)}
    
    Provide:
    1. Score (0-100%)
    2. Competency level
    3. Specific weak areas
    4. Improvement recommendations
    
    Response format (JSON):
    {{
        "score": 75,
        "level": "Intermediate", 
        "weak_areas": ["Concept A", "Concept B"],
        "recommendations": ["Practice X", "Study Y"]
    }}
    """
    
    try:
        raw_response = chat_with_openai(prompt, temperature=0.1)
        analysis_data = parse_json_response(raw_response)
        
        return SkillAnalysis(
            skill=skill,
            score=analysis_data.get("score", 0),
            level=analysis_data.get("level", "Beginner"),
            weak_areas=analysis_data.get("weak_areas", []),
            recommendations=analysis_data.get("recommendations", [])
        )
        
    except Exception as e:
        return SkillAnalysis(
            skill=skill,
            score=0,
            level="Error",
            weak_areas=[],
            recommendations=[f"Error analyzing {skill}: {str(e)}"]
        )
