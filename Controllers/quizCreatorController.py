from flask import request, jsonify
from Models.courseModel import CourseModel

import google.generativeai as genai
import os
import json

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
model = genai.GenerativeModel(model_name)


def generate_quiz():

    data = request.get_json()

    if not data:

        return jsonify({

            "success":False,

            "message":"No data received."

        }),400

    course_id = data.get("course_id")

    if not course_id:

        return jsonify({

            "success":False,

            "message":"Course ID is required."

        }),400

    course = CourseModel.get_course(course_id)

    if not course:

        return jsonify({

            "success":False,

            "message":"Course not found."

        }),404

    title = course.get("title", "").strip()
    description = course.get("description", "").strip()
    html_content = course.get("html_content", "").strip()

    # Bug #14 Fix: Fallback to html_content if course description is empty.
    # If both are empty, return a clean 400 error instead of sending an empty prompt to Gemini.
    if not description and html_content:
        description = html_content

    if not title and not description:
        return jsonify({
            "success": False,
            "message": "Cannot generate quiz: Course title and description/content are both empty."
        }), 400

    # Ensure Gemini API key is configured
    if not os.getenv("GEMINI_API_KEY"):
        return jsonify({
            "success": False,
            "message": "Quiz generation is currently unavailable: Gemini API key is not configured on the server."
        }), 500

    prompt = f"""
You are an expert Quantum Machine Learning instructor.

Generate a completely NEW quiz every time.

Course Title:
{title}

Course Description:
{description}

Rules:

1. Generate exactly 10 multiple choice questions.

2. Every question must have exactly 4 options.

3. Only ONE option is correct.

4. Shuffle correct answers.

5. Do not include explanations.

6. Return ONLY valid JSON.

Format:

{{
    "course":"{title}",
    "questions":[
        {{
            "question":"...",
            "options":[
                "...",
                "...",
                "...",
                "..."
            ],
            "correct_answer":"..."
        }}
    ]
}}

Return ONLY JSON.
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json","").replace("```","").strip()

        elif text.startswith("```"):
            text = text.replace("```","").strip()

        quiz = json.loads(text)

        return jsonify({

            "success":True,

            "quiz":quiz

        })

    except Exception as e:

        return jsonify({

            "success":False,

            "message":str(e)

        }),500