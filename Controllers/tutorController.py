import os

from flask import request, jsonify
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

genai.configure(

    api_key=os.getenv("GEMINI_API_KEY")

)

model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
model = genai.GenerativeModel(model_name)


def ask_tutor():

    try:

        data = request.get_json()

        # Ensure Gemini API key is configured
        if not os.getenv("GEMINI_API_KEY"):
            return jsonify({
                "success": False,
                "message": "AI Tutor is currently offline: Gemini API key is not configured on the server."
            }), 500

        if not data:

            return jsonify({

                "success": False,

                "message": "No data received."

            }),400

        question = data.get("question","").strip()

        if question == "":

            return jsonify({

                "success":False,

                "message":"Question is required."

            }),400

        prompt = f"""

You are an AI Tutor for a Quantum Machine Learning Learning Platform.

Rules:

- Answer clearly.
- Keep answer short.
- Maximum 200 words.
- If possible use bullet points.
- If question is about Quantum Computing, QML, Python, Qiskit or AI, explain like a teacher.
- Do not answer anything illegal.
- End with one learning tip.

Student Question:

{question}

"""

        response = model.generate_content(prompt)

        return jsonify({

            "success":True,

            "question":question,

            "answer":response.text

        })

    except Exception as e:

        return jsonify({

            "success":False,

            "message":str(e)

        }),500