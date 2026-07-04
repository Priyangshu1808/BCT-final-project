from chatbot.rag import retrieve_documents

docs = retrieve_documents("What is hostel fee?")

for doc in docs:
    print("=" * 50)
    print(doc.page_content)