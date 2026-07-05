from embeddings.vector_store import load_vector_db

vector_db = load_vector_db()


def retrieve_context(query, k=6):

    results = vector_db.similarity_search_with_score(query, k=k)

    # filter weak matches
    filtered = []

    for doc, score in results:
        # lower score = better match (Chroma behavior)
        if score < 1.2:
            filtered.append(doc)

    # fallback if nothing passes threshold
    if not filtered:
        filtered = [doc for doc, _ in results[:3]]

    context = ""

    for doc in filtered:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")

        context += f"""
SOURCE: {source} | PAGE: {page}

{doc.page_content}

---
"""

    return context, filtered