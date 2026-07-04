# # 

# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings

# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# DB_PATH = "db/chroma"

# def create_vector_db(chunks):
#     vectordb = Chroma.from_documents(
#         documents=chunks,
#         embedding=embedding_model,
#         persist_directory=DB_PATH,
#     )
#     return vectordb


# def load_vector_db():
#     return Chroma(
#         persist_directory=DB_PATH,
#         embedding_function=embedding_model,
#     )

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = "db/chroma"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_db(chunks):
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH,
    )
    return vectordb


def load_vector_db():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model,
    )