from embeddings.vector_store import load_vector_db
from langchain_community.document_loaders import PyPDFLoader
from loaders.text_splitter import split_documents
import os

vector_db = load_vector_db()


def retrieve_documents(query, k=3):
    results = vector_db.similarity_search_with_score(query, k=k)
    filtered = []
    for doc, score in results:
        # lower score = better match (Chroma behavior)
        if score < 1.2:
            filtered.append(doc)
    # fallback if nothing passes threshold
    if not filtered:
        filtered = [doc for doc, _ in results[:3]]
    return filtered


def retrieve_context(query, k=3):
    filtered = retrieve_documents(query, k=k)
    context = ""
    for doc in filtered:
        source = os.path.basename(doc.metadata.get("source", "Unknown"))
        page = doc.metadata.get("page", "N/A")

        context += f"""
SOURCE: {source} | PAGE: {page}

{doc.page_content}

---
"""

    return context, filtered


def index_new_pdf(pdf_path):
    global vector_db
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    chunks = split_documents(docs)
    
    # Add base metadata source name if not present
    for chunk in chunks:
        if "source" not in chunk.metadata:
            chunk.metadata["source"] = os.path.basename(pdf_path)
            
    vector_db.add_documents(chunks)
    return len(chunks), len(docs)