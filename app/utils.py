import pandas as pd
import json
from app.schemas import QuestionItem

def load_role_skills():
    df = pd.read_csv("app/data/role_skill_map.csv")
    role_map = {}
    for _, row in df.iterrows():
        role_map[row["role"]] = row["skills"].split(',')
    return role_map

def get_questions_by_skill(skill: str, difficulty: str):
    with open("app/data/sample_items.json") as f:
        items = json.load(f)
    
    mcqs = [QuestionItem(**q) for q in items.get(skill, {}).get(difficulty, {}).get("mcqs", [])]
    saqs = [QuestionItem(**q) for q in items.get(skill, {}).get(difficulty, {}).get("saqs", [])]
    aptitude = [QuestionItem(**q) for q in items.get(skill, {}).get(difficulty, {}).get("aptitude", [])]
    
    return {"mcqs": mcqs, "saqs": saqs, "aptitude": aptitude}
