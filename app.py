import streamlit as st
import os
import datetime

from rag.vector_store import create_vector_store
from rag.retriever import get_retriever
from chatbot_graph import create_graph

st.set_page_config(page_title="AI Admission Assistant", layout="wide")

st.title("University Website")
st.write("Welcome to our university portal. Use the AI assistant if you need help.")

# -----------------------------
# Session State
# -----------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Initialize AI system
# -----------------------------
vector_db = create_vector_store()
retriever = get_retriever(vector_db)
chat_graph = create_graph(retriever)

os.makedirs("data/logs", exist_ok=True)

# -----------------------------
# Floating AI Button Style
# -----------------------------
st.markdown("""
<style>
div.stButton > button:first-child {
    position: fixed;
    bottom: 20px;
    right: 20px;
    height: 100px;
    width: 100px;
    border-radius: 50%;
    font-size: 28px;
    background-color: #5c6cff;
    color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# AI Toggle Button
# -----------------------------
if st.button("🤖"):
    st.session_state.chat_open = not st.session_state.chat_open


# -----------------------------
# Chat Panel (Sidebar)
# -----------------------------
if st.session_state.chat_open:

    with st.sidebar:

        st.title("🎓 Admission Assistant")

        if st.button("Close Chat"):
            st.session_state.chat_open = False
            st.rerun()

        # Show chat history
        for msg in st.session_state.messages:

            avatar = "👤" if msg["role"] == "user" else "🎓"

            with st.chat_message(msg["role"], avatar=avatar):
                st.write(msg["content"])

        user_input = st.chat_input("Ask about admissions, courses, departments...")

        if user_input:

            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            with st.chat_message("user", avatar="👤"):
                st.write(user_input)

            # Log question
            with open("data/logs/questions.log", "a") as f:
                f.write(f"{datetime.datetime.now()} | {user_input}\n")

            result = chat_graph.invoke({
                "question": user_input
            })

            answer = result["answer"]

            with st.chat_message("assistant", avatar="🎓"):
                st.write(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
