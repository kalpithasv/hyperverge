from app.openai_client import chat_with_openai, parse_json_response
from app.schemas import AssessmentRequest, QuestionItem, AssessmentResponse
import json

def generate_assessment_from_ai(data: AssessmentRequest) -> AssessmentResponse:
    """
    Generate a comprehensive assessment using AI based on role, skills, and difficulty
    """
    
    # Create detailed prompt for assessment generation
    prompt = f"""
    You are an expert assessment generator for technical roles. Generate a comprehensive assessment based on the following requirements:

    ROLE: {data.role}
    SKILLS: {', '.join(data.skills)}
    DIFFICULTY LEVEL: {data.difficulty}

    REQUIREMENTS:
    1. Generate exactly 15 Multiple Choice Questions (MCQs)
    2. Generate exactly 5 Short Answer Questions (SAQs) 
    3. Generate exactly 1 Case Study/Scenario
    4. All questions must be appropriate for {data.difficulty} level
    5. Questions should cover all specified skills: {', '.join(data.skills)}
    6. MCQs should have 4 options (A, B, C, D) with one correct answer
    7. SAQs should be open-ended but specific
    8. Case study should be realistic and comprehensive

    DIFFICULTY GUIDELINES:
    - Beginner: Basic concepts, definitions, simple applications
    - Intermediate: Practical scenarios, analysis, problem-solving
    - Advanced: Complex scenarios, optimization, advanced concepts

    RESPONSE FORMAT (JSON):
    {{
        "mcqs": [
            {{
                "question": "Question text here",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "question_type": "MCQ",
                "skill": "Skill name",
                "difficulty": "{data.difficulty}",
                "points": 1
            }}
        ],
        "saqs": [
            {{
                "question": "Question text here",
                "correct_answer": "Expected answer or key points",
                "question_type": "SAQ",
                "skill": "Skill name", 
                "difficulty": "{data.difficulty}",
                "points": 2
            }}
        ],
        "case": {{
            "question": "Case study scenario and question",
            "correct_answer": "Expected approach and key points",
            "question_type": "Case",
            "skill": "Primary skill",
            "difficulty": "{data.difficulty}",
            "points": 5
        }}
    }}

    IMPORTANT: Ensure all questions are practical, relevant to the role, and test actual knowledge rather than memorization.
    """
    
    try:
        # Generate assessment using AI
        raw_response = chat_with_openai(prompt, temperature=0.3)
        assessment_data = parse_json_response(raw_response)
        
        # Validate and structure the response
        mcqs = [QuestionItem(**q) for q in assessment_data.get("mcqs", [])]
        saqs = [QuestionItem(**q) for q in assessment_data.get("saqs", [])]
        case = QuestionItem(**assessment_data.get("case", {}))
        
        # Calculate total questions and skills covered
        total_questions = len(mcqs) + len(saqs) + 1
        skills_covered = list(set([q.skill for q in mcqs + saqs + [case]]))
        
        return AssessmentResponse(
            mcqs=mcqs,
            saqs=saqs,
            case=case,
            total_questions=total_questions,
            difficulty=data.difficulty,
            skills_covered=skills_covered
        )
        
    except Exception as e:
        raise ValueError(f"Failed to generate assessment: {str(e)}")

def generate_demotion_assessment(role: str, skills: list, target_difficulty: str = "Beginner") -> AssessmentResponse:
    """
    Generate a simplified assessment for users who need to be demoted to a lower level
    """
    
    prompt = f"""
    Generate a simplified assessment for a user who needs to start with {target_difficulty} level material.

    ROLE: {role}
    SKILLS: {', '.join(skills)}
    TARGET DIFFICULTY: {target_difficulty}

    Generate:
    - 10 MCQs (basic concepts only)
    - 3 SAQs (fundamental understanding)
    - 1 Simple case study

    Focus on foundational concepts and basic applications. Make questions straightforward and educational.
    """
    
    try:
        raw_response = chat_with_openai(prompt, temperature=0.2)
        assessment_data = parse_json_response(raw_response)
        
        mcqs = [QuestionItem(**q) for q in assessment_data.get("mcqs", [])]
        saqs = [QuestionItem(**q) for q in assessment_data.get("saqs", [])]
        case = QuestionItem(**assessment_data.get("case", {}))
        
        return AssessmentResponse(
            mcqs=mcqs,
            saqs=saqs,
            case=case,
            total_questions=len(mcqs) + len(saqs) + 1,
            difficulty=target_difficulty,
            skills_covered=list(set([q.skill for q in mcqs + saqs + [case]]))
        )
        
    except Exception as e:
        raise ValueError(f"Failed to generate demotion assessment: {str(e)}")
