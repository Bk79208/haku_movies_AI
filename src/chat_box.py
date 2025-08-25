# chat_box.py
import streamlit as st
from src.movie_genre_rag import rag_answer  # import our RAG helper


def submit_message():
    user_msg = st.session_state.chat_input.strip()
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})

        # 🔥 call the RAG pipeline
        answer = rag_answer(user_msg, chat_history=st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # clear input box
    st.session_state.chat_input = ""


def chatbox():
    with st.sidebar:
        st.markdown("### 🤖 Chat Assistant")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # show previous messages
        for m in st.session_state.chat_history:
            if m["role"] == "user":
                st.write(f"**You:** {m['content']}")
            else:
                st.write(f"**K:** {m['content']}")

        # input field with callback
        st.text_input(
            "Ask me about movies...",
            key="chat_input",
            on_change=submit_message
        )




    # Floating Chat Box
    # chatbox = """
    # <style>
    # .chat-box {
    #     position: fixed;
    #     bottom: 20px;
    #     right: 20px;
    #     width: 300px;
    #     background: white;
    #     border: 2px solid #ddd;
    #     border-radius: 10px;
    #     padding: 10px;
    #     box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    #     z-index: 9999;
    # }
    # </style>

    # <div class="chat-box">
    #     <h4>🤖 Chat Assistant</h4>
    #     <input type="text" id="chat_input" placeholder="Ask me about movies..." style="width:100%; padding:5px;">
    #     <p style="font-size:12px; color:gray;">(Floating box mockup – input won’t work yet)</p>
    # </div>
    # """

    # st.markdown(chatbox, unsafe_allow_html=True)

    # --- put this anywhere in your page after your main content ---
    # 1) Invisible anchor to target with CSS
    # st.markdown('<div id="chat_anchor"></div>', unsafe_allow_html=True)

    # # 2) The actual chat UI (this whole block will be floated by CSS below)
    # with st.container():
    #     st.markdown("### 🤖 Chat Assistant")
    #     if "messages" not in st.session_state:
    #         st.session_state.messages = []

    #     # history (optional)
    #     for m in st.session_state.messages:
    #         st.write(f"**{m['role'].title()}:** {m['content']}")

    #     user_msg = st.text_input("Ask me about movies...", key="chat_floating_input")
    #     if user_msg:
    #         st.session_state.messages.append({"role": "user", "content": user_msg})
    #         # TODO: call your agent here and append assistant reply to messages
    #         st.rerun()

    # # 3) CSS: fix the chat block (the block right after #chat_anchor) to bottom-right
    # st.markdown("""
    # <style>
    # /* Style the Streamlit block that immediately follows our anchor */
    # #chat_anchor + div[data-testid="stVerticalBlock"] {
    #     position: fixed;
    #     bottom: 16px;
    #     right: 16px;
    #     width: 340px;
    #     max-height: 60vh;
    #     overflow: auto;
    #     background: var(--background-color);
    #     border: 1px solid rgba(49,51,63,0.2);
    #     border-radius: 12px;
    #     padding: 12px;
    #     box-shadow: 0 8px 24px rgba(0,0,0,.25);
    #     z-index: 1000;
    # }

    # /* Optional: make the label smaller to save space */
    # #chat_anchor + div[data-testid="stVerticalBlock"] label {
    #     font-size: 0.9rem;
    # }
    # </style>
    # """, unsafe_allow_html=True)