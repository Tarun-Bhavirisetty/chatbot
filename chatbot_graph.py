from langgraph.graph import StateGraph
from typing import TypedDict
from langchain_groq import ChatGroq
import os
import streamlit as st
from dotenv import load_dotenv

# Load .env for local
load_dotenv()


class ChatState(TypedDict):
    question: str
    context: str
    answer: str


def create_graph(retriever):

    # ✅ Works for both local (.env) and Streamlit Cloud (secrets)
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=api_key
    )

    def retrieve(state):
        docs = retriever.invoke(state["question"])

        if not isinstance(docs, list):
            docs = [docs]

        context = "\n".join([doc.page_content for doc in docs])
        return {"context": context}

    def generate(state):

        prompt = f"""
You are an AI university admission assistant.

Your job is to help students with questions about the university.

RULES:
1. If the question is a greeting or general conversation, respond politely.
2. If the question is about university info, answer ONLY from context.
3. Do NOT invent facts.
4. If not found, say: "I don't have that information."
5. Keep answers short.

Context:
{state['context']}

Question:
{state['question']}
"""

        response = llm.invoke(prompt)
        return {"answer": response.content}

    graph = StateGraph(ChatState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")

    return graph.compile()