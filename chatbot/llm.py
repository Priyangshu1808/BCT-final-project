import os
from google.api_core.exceptions import ResourceExhausted
import google.generativeai as genai
from dotenv import load_dotenv
from chatbot.prompts import SYSTEM_PROMPT

load_dotenv()

# Resolve API key from environment variables or Streamlit secrets fallback
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("gemini_api_key")
    except Exception:
        pass

genai.configure(api_key=api_key, transport="rest")

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(question, context, history=None):
    history_str = ""
    if history:
        for msg in history[-6:]:  # include last 3 turns (6 messages)
            role_label = "USER" if msg["role"] == "user" else "ASSISTANT"
            history_str += f"{role_label}: {msg['content']}\n"

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

CONVERSATION HISTORY:
{history_str}
USER: {question}
ASSISTANT:
"""

    try:
        response = model.generate_content(prompt)

        return response.text

    except ResourceExhausted:
        return (
            "⚠️ Gemini API quota exceeded.\n\n"
            "Please wait until your quota resets or use another API key."
        )

    except Exception as e:
        return f"Error: {str(e)}"