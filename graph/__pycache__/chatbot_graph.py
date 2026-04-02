from langgraph.graph import StateGraph
from typing import TypedDict
from langchain_groq import ChatGroq


class ChatState(TypedDict):

    question: str
    context: str
    answer: str


def create_graph(retriever):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key="your_key"
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

1. If the question is a greeting or general conversation (like "hi", "hello", "who are you", "tell me about yourself"),
   respond politely as a university admission assistant.

2. If the question is about university information (departments, courses, admissions, facilities, etc),
   answer using ONLY the provided context.

3. Do NOT invent facts.

4. If the answer cannot be found in the context, reply:
"I don't have that information."

5. Keep answers clear and short.

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
