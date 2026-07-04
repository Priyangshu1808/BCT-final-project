from loaders.pdf_loader import load_documents
from loaders.text_splitter import split_documents
from embeddings.vector_store import create_vector_db


documents = load_documents("data/pdfs")

chunks = split_documents(documents)

create_vector_db(chunks)

print("Knowledge Base Created Successfully!")