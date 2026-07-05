import os
import requests
from dotenv import load_dotenv
from chatbot.prompts import SYSTEM_PROMPT

load_dotenv()

# Resolve Grok API key from environment variables or Streamlit secrets
api_key = os.getenv("XAI_API_KEY")
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("XAI_API_KEY") or st.secrets.get("xai_api_key")
    except Exception:
        pass


def ask_grok(question, context, history=None):
    if not api_key:
        return (
            "⚠️ Grok API key is not configured.\n\n"
            "Please add `XAI_API_KEY` to your environment variables or Streamlit Secrets."
        )

    history_messages = []
    if history:
        for msg in history[-6:]:  # include last 3 turns
            role = "user" if msg["role"] == "user" else "assistant"
            history_messages.append({"role": role, "content": msg["content"]})

    # Combine query with context
    prompt = f"""
CONTEXT:
{context}

USER: {question}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2",
        "messages": messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            return "⚠️ xAI API authentication failed. Please verify your XAI_API_KEY."
        elif response.status_code == 429:
            return "⚠️ xAI API rate limit exceeded."
        else:
            return f"HTTP Error: {http_err}"
    except Exception as e:
        return f"Error calling Grok API: {str(e)}"