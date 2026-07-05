import os
import google.generativeai as genai
from dotenv import load_dotenv
from chatbot.prompts import SYSTEM_PROMPT

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(question, context):

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,   # 🔥 more factual
            "top_p": 0.9
        }
    )

    return response.text