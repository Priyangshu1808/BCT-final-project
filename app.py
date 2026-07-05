import streamlit as st
from chatbot.llm import ask_gemini
from chatbot.rag import retrieve_context

st.set_page_config(page_title="CampusGPT", page_icon="🎓", layout="wide")

st.title("🎓 CampusGPT")
st.caption("AI-powered College Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# sidebar
with st.sidebar:
    st.title("Controls")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# show chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask about your college...")

if query:

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner("Searching knowledge base... 🔍"):

            context, docs = retrieve_context(query)

        with st.spinner("Generating answer... 🤖"):

            answer = ask_gemini(query, context)

        st.markdown(answer)

        with st.expander("📄 Sources"):
            for doc in docs:
                st.write(
                    f"📘 {doc.metadata.get('source')} "
                    f"(Page {doc.metadata.get('page', 'N/A')})"
                )

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )