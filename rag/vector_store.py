import os
from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embeddings
from utils.metadata_loader import load_all_documents

FAISS_PATH = "faiss_index"

def create_vector_store():

    embeddings = get_embeddings()

    if os.path.exists(FAISS_PATH):

        vector_db = FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        return vector_db

    docs = load_all_documents()

    vector_db = FAISS.from_documents(docs, embeddings)

    vector_db.save_local(FAISS_PATH)

    return vector_db