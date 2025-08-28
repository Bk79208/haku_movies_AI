import os
import streamlit as st
from dotenv import load_dotenv
from pinecone import Pinecone
from src.create_vectors import embed_text, vector_index
from groq import Groq
from src.recommend import recommendFromGenres

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY)
def chatbox():
    # App title
    st.title("🎬 AI chat Assistant")

    # System prompt
    system_prompt = {
        "role": "system",
        "content": (
            "You're a movie assistant named K. "
            "Only use the provided documents to answer. "
            "If unsure, say: 'Not found in documents.'"
        )
    }

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [system_prompt]

    # Display previous messages with styling
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            # st.markdown(message["content"])
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: flex-end;
                    margin: 10px 0;
                ">
                    <div style="
                        background-color: black;
                        color: white;
                        padding: 10px 15px;
                        border-radius: 10px;
                        max-width: 75%;
                        word-wrap: break-word;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    ">
                        {message['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Input field
    if user_input := st.chat_input("Ask me anything about movies..."):
        # Show user input
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin: 10px 0;
            ">
                <div style="
                    background-color: black;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 10px;
                    max-width: 75%;
                    word-wrap: break-word;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    {user_input}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})


        # --- RAG retrieval ---
        vector = embed_text(user_input).get("embedding", [])
        response = vector_index.query(vector=vector, top_k=2, include_metadata=True)

        similar_document = ""
        for match in response["matches"]:
            doc_text = match["metadata"]["text"][:1000]  # Limit to 1000 chars
            similar_document += doc_text + "\n"

        # If no relevant documents, optionally fallback to web search (Optional)
        if not similar_document.strip():
            similar_document = "No relevant documents found."
            # Optional fallback: Web search (placeholder)
            # from serpapi import GoogleSearch
            # search = GoogleSearch({"q": user_input, "api_key": SERPAPI_KEY})
            # results = search.get_dict()
            # similar_document += "\nWeb result: " + results.get("organic_results", [])[0]["snippet"]

        # Construct message for LLM
        query_message = {
            "role": "user",
            "content": f"""
            You are given several documents about movies. 
            Answer the user query truthfully using only the information from the documents.  
            If the answer is not in the documents, reply with: "Not found in documents".

            Documents:
            {similar_document}

            User query: {user_input}

            Answering rules:

            1. **Movie list queries**  
            - Start with a short descriptive sentence that naturally rephrases the user query.  
            - Then, list movie names as an unordered Markdown list using "-".

            2. **Person queries (actor/director)**  
            - Give a short description about the person using the documents, mentioning role and key works.

            3. **Mixed queries (both person + movies)**  
            - Combine description and movie list as above.
            """
        }

        # Build full message list
        # full_messages = st.session_state.chat_history[:-1] + [query_message]

        # Only keep system + last 3 exchanges + current prompt
        chat_memory = st.session_state.chat_history
        short_history = [chat_memory[0]] + chat_memory[-6:]  # system + last 3 pairs
        full_messages = short_history + [query_message]


        # Call LLM
        llm_response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=full_messages,
            max_tokens=500,
            temperature=0.7,
        )

        # Extract and display response
        assistant_reply = llm_response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
