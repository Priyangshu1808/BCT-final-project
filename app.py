import streamlit as st
import os
from chatbot.llm import ask_gemini
from chatbot.rag import retrieve_context, index_new_pdf

st.set_page_config(
    page_title="CampusGPT | AI College Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium glassmorphic/dark theme aesthetic
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Header styling */
    .main-title {
        font-size: 3.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 10%, #a855f7 50%, #ec4899 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
        text-align: center;
        letter-spacing: -0.05em;
    }
    .main-subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Sidebar customization */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Card design for suggest questions */
    .quick-start-title {
        font-weight: 600;
        color: #cbd5e1;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1.1rem;
    }
    
    /* Chat layout styling */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 18px 24px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        transition: border-color 0.25s ease;
    }
    div[data-testid="stChatMessage"]:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
    }
    
    /* User Message distinct background */
    div[data-testid="stChatMessage"][data-testid="user"] {
        background: rgba(99, 102, 241, 0.08) !important;
        border-color: rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Message font size */
    div[data-testid="stChatMessageContent"] {
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Sources style */
    .source-badge {
        background-color: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-bottom: 8px;
        display: inline-block;
        font-weight: 500;
        transition: transform 0.2s ease;
    }
    .source-badge:hover {
        transform: translateY(-1px);
        background-color: rgba(99, 102, 241, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# Main Title Logo
st.markdown('<div class="main-title">🎓 CampusGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">AI-powered College Assistant with conversational RAG intelligence</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_query" not in st.session_state:
    st.session_state.quick_query = None

# Sidebar Content
with st.sidebar:
    st.markdown("### ⚙️ System Control Room")
    
    if st.button("🗑 Clear Conversation History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.quick_query = None
        st.success("Chat history cleared!")
        st.rerun()
        
    st.markdown("---")
    
    # PDF Uploader & Reindexing
    st.markdown("### 📥 Dynamic PDF Indexer")
    uploaded_file = st.file_uploader("Upload college notice or document (PDF)", type=["pdf"])
    if uploaded_file is not None:
        file_path = os.path.join("data/pdfs", uploaded_file.name)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Parsing & embedding document..."):
                try:
                    chunks_added, pages_added = index_new_pdf(file_path)
                    st.success(f"Indexed successfully! {pages_added} pages ({chunks_added} chunks) added.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error parsing PDF: {e}")
        else:
            st.info(f"'{uploaded_file.name}' is already indexed.")
            
    st.markdown("---")
    
    # Show stats of loaded documents
    pdf_files = [f for f in os.listdir("data/pdfs") if f.endswith(".pdf")]
    st.markdown(f"### 📚 Indexed Documents ({len(pdf_files)})")
    for pdf in pdf_files:
        st.markdown(f"🔹 **{pdf}**")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Quick-Start Suggestions (only visible if chat history is empty)
if len(st.session_state.messages) == 0 and st.session_state.quick_query is None:
    st.markdown('<div class="quick-start-title">💡 Click a suggestion to query immediately:</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 Academic Calendar: View semester milestones, exams & events", use_container_width=True):
            st.session_state.quick_query = "What are the key events and dates in the academic calendar?"
        if st.button("💼 Placements: Show recent employment and top hiring partners", use_container_width=True):
            st.session_state.quick_query = "What is the placement status and top recruiters?"
    with col2:
        if st.button("🎓 Admissions: How to apply, eligible criteria & key dates", use_container_width=True):
            st.session_state.quick_query = "What are the details of the admissions process and eligibility criteria?"
        if st.button("🏠 Hostel Regulations: Rules, boarding details & fees", use_container_width=True):
            st.session_state.quick_query = "What are the hostel regulations, facilities, and fees?"

# Get search input (either from suggestion buttons or chat box)
query = st.chat_input("Ask about Admissions, Fees, Exams, Hostel, and Placements...")

# If a quick start button was clicked, use it
if st.session_state.quick_query:
    query = st.session_state.quick_query
    st.session_state.quick_query = None # clear it for next turns

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Consulting the college knowledge base... 🔍"):
            context, docs = retrieve_context(query)
            
        with st.spinner("Synthesizing answer... 🤖"):
            answer = ask_gemini(query, context, history=st.session_state.messages[:-1])
            
        st.markdown(answer)
        
        # Style and render sources beautifully
        if docs:
            st.markdown("##### 📄 Reference Sources:")
            source_html = ""
            seen_sources = set()
            for doc in docs:
                src_name = os.path.basename(doc.metadata.get("source", "Unknown"))
                page_num = doc.metadata.get("page", "N/A")
                
                # Check for duplicates or page ranges
                key = (src_name, page_num)
                if key not in seen_sources:
                    seen_sources.add(key)
                    # Convert pages to display friendly format
                    page_disp = f"Page {page_num + 1}" if isinstance(page_num, int) else f"Page {page_num}"
                    source_html += f'<span class="source-badge">📘 {src_name} ({page_disp})</span>'
            st.markdown(source_html, unsafe_allow_html=True)
            
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()