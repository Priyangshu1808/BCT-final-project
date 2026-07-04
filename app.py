import streamlit as st
from chatbot.llm import ask_gemini
from chatbot.rag import retrieve_context

st.set_page_config(
    page_title="CampusGPT",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 CampusGPT")
st.caption("Your AI College Assistant")

# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Display Previous Messages
# -------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# User Input
# -------------------------

prompt = st.chat_input("Ask me anything about your college...")

if prompt:

    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Retrieve Context
    with st.spinner("Searching documents..."):
        context, docs = retrieve_context(prompt)

        answer = ask_gemini(prompt, context)

    # Show Assistant Message
    with st.chat_message("assistant"):
        st.markdown(answer)

        with st.expander("📄 Sources"):
            for doc in docs:
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                st.write(f"📄 {source} | Page {page}")

    # Save Assistant Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )