def get_retriever(vector_db):

    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 20,
            "fetch_k": 50
        }
    )

    return retriever