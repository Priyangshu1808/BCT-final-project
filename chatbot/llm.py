import os
from google.api_core.exceptions import ResourceExhausted
import google.generativeai as genai
from dotenv import load_dotenv
from chatbot.prompts import SYSTEM_PROMPT

load_dotenv()

# Resolve API key from environment variables or Streamlit secrets fallback
api_key_raw = os.getenv("GEMINI_API_KEY")
if not api_key_raw:
    try:
        import streamlit as st
        api_key_raw = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("gemini_api_key")
    except Exception:
        pass

# Parse comma-separated keys for API key rotation
api_keys = [k.strip() for k in api_key_raw.split(",") if k.strip()] if api_key_raw else []
current_key_idx = 0

# Set initial default configuration
if api_keys:
    genai.configure(api_key=api_keys[0], transport="rest")


def ask_gemini(question, context, history=None):
    if not api_keys:
        return (
            "⚠️ Gemini API key is not configured.\n\n"
            "Please add `GEMINI_API_KEY` to your environment variables or Streamlit Secrets."
        )

    global current_key_idx
    history_str = ""
    if history:
        for msg in history[-4:]:  # include last 2 turns (4 messages)
            role_label = "USER" if msg["role"] == "user" else "ASSISTANT"
            history_str += f"{role_label}: {msg['content']}\n"

    prompt = f"""
CONTEXT:
{context}

CONVERSATION HISTORY:
{history_str}
USER: {question}
ASSISTANT:
"""

    last_error = ""
    # Loop over all configured keys if they exhaust their limits
    for _ in range(len(api_keys)):
        active_key = api_keys[current_key_idx]
        try:
            genai.configure(api_key=active_key, transport="rest")
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=SYSTEM_PROMPT
            )
            response = model.generate_content(prompt)
            return response.text
        except ResourceExhausted as e:
            last_error = str(e)
            current_key_idx = (current_key_idx + 1) % len(api_keys)
            continue
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "quota" in err_msg.lower() or "limit" in err_msg.lower():
                last_error = err_msg
                current_key_idx = (current_key_idx + 1) % len(api_keys)
                continue
            return f"Error: {err_msg}"

    return (
        "⚠️ Gemini API quota exceeded on all configured keys.\n\n"
        f"Details of last failure: {last_error}"
    )