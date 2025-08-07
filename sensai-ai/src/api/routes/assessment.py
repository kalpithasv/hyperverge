import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
from api.settings import settings

router = APIRouter()

class AssessmentRequest(BaseModel):
    role: str
    skills: List[str]
    difficulty: str
    include_minicase: Optional[bool] = True
    include_aptitude: Optional[bool] = True

def build_prompt(data: AssessmentRequest) -> str:
    return f"""
You are an AI that generates job assessments based on the following input.

role: {data.role}
skills: {data.skills}
difficulty: {data.difficulty}
include_minicase: {data.include_minicase}
include_aptitude: {data.include_aptitude}

Generate a JSON with:
- 15 MCQs
- 5 SAQs
- 1 Mini-case (if included)
- 6-8 aptitude questions (if included)
- Skill coverage summary (json)

Output only valid JSON strictly matching the required format.
    """

@router.post("/assessment/generate")
async def generate_assessment(data: AssessmentRequest):
    try:
        prompt = build_prompt(data)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message["content"]
        
        # Parse the LLM response as JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"LLM did not return valid JSON: {str(e)}")
        
        # Validate that the response has the required fields
        if not isinstance(result, dict):
            raise HTTPException(status_code=500, detail="LLM response is not a JSON object")
        
        # Check for assessment field (could be named differently)
        assessment = None
        coverage_report = None
        
        # Look for common field names
        if "assessment" in result:
            assessment = result["assessment"]
        elif "questions" in result:
            assessment = result["questions"]
        elif "items" in result:
            assessment = result["items"]
        
        if "coverage_report" in result:
            coverage_report = result["coverage_report"]
        elif "coverage" in result:
            coverage_report = result["coverage"]
        elif "summary" in result:
            coverage_report = result["summary"]
        
        if not assessment or not coverage_report:
            # If we can't find the expected fields, return the raw result
            # but structure it properly for the frontend
            return {
                "assessment": result.get("assessment", result.get("questions", result.get("items", []))),
                "coverage_report": result.get("coverage_report", result.get("coverage", result.get("summary", {})))
            }
        
        return {
            "assessment": assessment,
            "coverage_report": coverage_report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
