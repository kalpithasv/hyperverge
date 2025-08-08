from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AssessmentRequest(BaseModel):
    role: str
    skills: List[str]
    difficulty: str  # "Beginner", "Intermediate", "Advanced"

class QuestionItem(BaseModel):
    question: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    question_type: str  # "MCQ", "SAQ", "Case"
    skill: str
    difficulty: str
    points: int = 1

class AssessmentResponse(BaseModel):
    mcqs: List[QuestionItem]
    saqs: List[QuestionItem]
    case: QuestionItem
    total_questions: int
    difficulty: str
    skills_covered: List[str]

class AnswerItem(BaseModel):
    question: str
    user_answer: str
    question_type: str
    skill: str
    difficulty: str

class AssessmentSubmission(BaseModel):
    difficulty: str
    responses: List[AnswerItem]
    role: str
    skills: List[str]

class UserFeedback(BaseModel):
    score: int
    actual_level: str
    message: str
    skill_breakdown: Dict[str, Dict[str, Any]]
    recommendations: List[str]
    should_demote: bool
    suggested_assessment: Optional[str] = None

class SkillAnalysis(BaseModel):
    skill: str
    score: int
    level: str
    weak_areas: List[str]
    recommendations: List[str]
