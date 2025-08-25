# movie_genre_rag.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from src.create_vectors import embed_text, vector_index
from groq import Groq

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)

def rag_answer(user_input, chat_history=None):
    """Generate RAG-based response from Pinecone + Groq LLM."""

    # --- RAG retrieval ---
    vector = embed_text(user_input).get("embedding", [])
    response = vector_index.query(vector=vector, top_k=2, include_metadata=True)

    similar_document = ""
    for match in response["matches"]:
        doc_text = match["metadata"]["text"][:1000]
        similar_document += doc_text + "\n"

    if not similar_document.strip():
        similar_document = "No relevant documents found."

    query_message = {
        "role": "user",
        "content": f"""
        You are given several documents about movies. 
        Answer the user query truthfully using only the information from the documents.  
        If the answer is not in the documents, reply with: "Not found in documents".

        Documents:
        {similar_document}

        User query: {user_input}
        """
    }

    system_prompt = {
        "role": "system",
        "content": (
            "You're a movie assistant named K. "
            "Only use the provided documents to answer. "
            "If unsure, say: 'Not found in documents.'"
        )
    }

    if chat_history is None:
        chat_history = [system_prompt]

    short_history = [chat_history[0]] + chat_history[-6:]
    full_messages = short_history + [query_message]

    llm_response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=full_messages,
        max_tokens=500,
        temperature=0.7,
    )

    return llm_response.choices[0].message.content
