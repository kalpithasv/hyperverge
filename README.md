# Hyperverge


Here’s a concise and clean README for the 3rd problem statement ("AI Assistant for Course Creators"):

---

# Hyperverge AI Assistant for Course Creators

This project is built for the HyperVerge SenseAI Hackathon 2025. It addresses the problem statement: **AI Assistant for Course Creators**.

## Problem Statement

Course creators often struggle with building effective, personalized assessments aligned to job roles, skills, and learning goals. Our solution streamlines this process using AI to automate assessment creation and learner feedback.

## Features

* **Role & Skill-Aligned Assessment Generator**

  * Input: job role, skill list, and difficulty level
  * Output: 15 MCQs, 5 SAQs, 1 mini-case, optional aptitude questions
* **Skill Coverage Matrix**

  * Ensures all skills are tested proportionally
* **Dynamic Difficulty Calibration**

  * Adjusts question complexity per input level
* **Post-Assessment Analytics**

  * Scores user answers and recommends level adjustments
* **Frontend Integration**

  * In-app test creation, test preview, and result analysis

## Tech Stack

* **Frontend**: Next.js, Tailwind CSS
* **Backend**: FastAPI (Python), SQLite
* **AI**: OpenAI API (GPT-4)
* **Hosting**: Netlify (frontend), Render (backend)

## Local Setup

```bash
# Clone repo
git clone https://github.com/kalpithasv/hyperverge.git
cd hyperverge

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd ../frontend
npm install
npm run dev
```

## Deployment

* Frontend: [Netlify Link](https://funny-cuchufli-1d057b.netlify.app/)
* Backend: Hosted via Render

## Status

* ✅ Core backend working (assessment generation & analytics)
* ✅ Frontend integrated with backend
* ⏳ In-progress: Auto-difficulty adjustment, user history tracking

---

Let me know if you want to split it into sections for frontend/backend separately or add visual examples.
