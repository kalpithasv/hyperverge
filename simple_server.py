from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

# Set up OpenAI
openai.api_key = "sk-aquejIxDfXWhe_-VJxMmbA"
openai.api_base = "https://agent.dev.hyperverge.org"

def generate_assessment(role, skills, difficulty):
    """Generate assessment using OpenAI"""
    prompt = f"""
    You are an expert assessment generator for technical roles. Generate a comprehensive assessment based on the following requirements:

    ROLE: {role}
    SKILLS: {', '.join(skills)}
    DIFFICULTY LEVEL: {difficulty}

    REQUIREMENTS:
    1. Generate exactly 15 Multiple Choice Questions (MCQs)
    2. Generate exactly 5 Short Answer Questions (SAQs) 
    3. Generate exactly 1 Case Study/Scenario
    4. All questions must be appropriate for {difficulty} level
    5. Questions should cover all specified skills: {', '.join(skills)}
    6. MCQs should have 4 options (A, B, C, D) with one correct answer
    7. SAQs should be open-ended but specific
    8. Case study should be realistic and comprehensive

    RESPONSE FORMAT (JSON):
    {{
        "mcqs": [
            {{
                "question": "Question text here",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "question_type": "MCQ",
                "skill": "Skill name",
                "difficulty": "{difficulty}",
                "points": 1
            }}
        ],
        "saqs": [
            {{
                "question": "Question text here",
                "correct_answer": "Expected answer or key points",
                "question_type": "SAQ",
                "skill": "Skill name", 
                "difficulty": "{difficulty}",
                "points": 2
            }}
        ],
        "case": {{
            "question": "Case study scenario and question",
            "correct_answer": "Expected approach and key points",
            "question_type": "Case",
            "skill": "Primary skill",
            "difficulty": "{difficulty}",
            "points": 5
        }}
    }}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON response
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            json_str = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            json_str = content[start:end].strip()
        else:
            json_str = content.strip()
        
        data = json.loads(json_str)
        
        # Calculate totals
        total_questions = len(data.get("mcqs", [])) + len(data.get("saqs", [])) + 1
        skills_covered = list(set([q.get("skill", "") for q in data.get("mcqs", []) + data.get("saqs", []) + [data.get("case", {})]]))
        
        return {
            "mcqs": data.get("mcqs", []),
            "saqs": data.get("saqs", []),
            "case": data.get("case", {}),
            "total_questions": total_questions,
            "difficulty": difficulty,
            "skills_covered": skills_covered
        }
        
    except Exception as e:
        return {"error": f"Failed to generate assessment: {str(e)}"}

def evaluate_answers(assessment_data, user_answers, role, skills, difficulty):
    """Evaluate user answers and generate comprehensive analytics"""
    
    # Prepare the assessment data for evaluation
    all_questions = []
    for mcq in assessment_data.get("mcqs", []):
        all_questions.append({
            "question": mcq["question"],
            "correct_answer": mcq["correct_answer"],
            "question_type": mcq["question_type"],
            "skill": mcq["skill"],
            "difficulty": mcq["difficulty"],
            "points": mcq["points"]
        })
    
    for saq in assessment_data.get("saqs", []):
        all_questions.append({
            "question": saq["question"],
            "correct_answer": saq["correct_answer"],
            "question_type": saq["question_type"],
            "skill": saq["skill"],
            "difficulty": saq["difficulty"],
            "points": saq["points"]
        })
    
    all_questions.append({
        "question": assessment_data["case"]["question"],
        "correct_answer": assessment_data["case"]["correct_answer"],
        "question_type": assessment_data["case"]["question_type"],
        "skill": assessment_data["case"]["skill"],
        "difficulty": assessment_data["case"]["difficulty"],
        "points": assessment_data["case"]["points"]
    })
    
    # Create evaluation prompt
    evaluation_prompt = f"""
    You are an expert assessment evaluator. Analyze the following assessment responses and provide comprehensive feedback.

    ASSESSMENT CONTEXT:
    - Role: {role}
    - Skills Tested: {', '.join(skills)}
    - Difficulty Level: {difficulty}

    QUESTIONS AND ANSWERS:
    """
    
    for i, question in enumerate(all_questions):
        user_answer = next((ans["user_answer"] for ans in user_answers if ans["question"] == question["question"]), "")
        evaluation_prompt += f"""
        Question {i+1} ({question['question_type']} - {question['skill']}):
        Question: {question['question']}
        Expected Answer: {question['correct_answer']}
        User Answer: {user_answer}
        Points: {question['points']}
        """
    
    evaluation_prompt += """
    
    Please provide a comprehensive evaluation in the following JSON format:
    {
        "score": 75,
        "actual_level": "Intermediate",
        "message": "Detailed AI-generated feedback about the user's performance...",
        "skill_breakdown": {
            "SQL": {
                "score": 8,
                "total_possible": 10,
                "percentage": 80,
                "level": "Intermediate",
                "weak_areas": ["Complex joins", "Window functions"],
                "recommendations": ["Practice advanced SQL queries", "Learn window functions"]
            }
        },
        "recommendations": [
            "General recommendation 1",
            "General recommendation 2"
        ],
        "should_demote": false,
        "suggested_assessment": "Intermediate"
    }
    
    EVALUATION GUIDELINES:
    1. Score should be 0-100 based on accuracy and completeness
    2. Actual level should be Beginner/Intermediate/Advanced based on performance
    3. Provide detailed skill breakdown for each tested skill
    4. Identify specific weak areas and provide actionable recommendations
    5. Consider the difficulty level when evaluating
    6. Be encouraging but honest about areas for improvement
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": evaluation_prompt}],
            temperature=0.3,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON response
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            json_str = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            json_str = content[start:end].strip()
        else:
            json_str = content.strip()
        
        return json.loads(json_str)
        
    except Exception as e:
        return {"error": f"Failed to evaluate answers: {str(e)}"}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "AI Assessment System"})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        role = data.get('role', '')
        skills = data.get('skills', [])
        difficulty = data.get('difficulty', 'Beginner')
        
        if not role or not skills:
            return jsonify({"error": "Role and skills are required"}), 400
        
        result = generate_assessment(role, skills, difficulty)
        
        if "error" in result:
            return jsonify({"detail": result["error"]}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"detail": f"Failed to generate assessment: {str(e)}"}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.get_json()
        assessment_data = data.get('assessment', {})
        user_answers = data.get('responses', [])
        role = data.get('role', '')
        skills = data.get('skills', [])
        difficulty = data.get('difficulty', 'Beginner')
        
        if not assessment_data or not user_answers:
            return jsonify({"error": "Assessment data and user answers are required"}), 400
        
        result = evaluate_answers(assessment_data, user_answers, role, skills, difficulty)
        
        if "error" in result:
            return jsonify({"detail": result["error"]}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"detail": f"Failed to evaluate assessment: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "AI Assessment System API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate - Generate assessment",
            "evaluate": "/evaluate - Evaluate answers and generate analytics",
            "health": "/health - Health check"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
