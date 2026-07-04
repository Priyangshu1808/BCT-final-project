import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


SYSTEM_PROMPT = """
You are CampusGPT, an AI assistant for a college.

Rules:

1. Answer ONLY from the provided context.
2. Never make up information.
3. If the answer isn't present, say:
   "I couldn't find this information in the uploaded college documents."
4. Format answers clearly.
5. Use bullet points whenever appropriate.
"""


def ask_gemini(question, context):

    prompt = f"""
{SYSTEM_PROMPT}

Context:

{context}

Question:

{question}

Answer:
"""

    response = model.generate_content(prompt)

    return response.text