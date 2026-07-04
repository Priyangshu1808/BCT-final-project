from embeddings.vector_store import load_vector_db

vectordb = load_vector_db()


def retrieve_context(query, k=4):

    docs = vectordb.similarity_search(query, k=k)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context, docs