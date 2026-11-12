import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

from database import save_message, load_messages, clear_chat

# ==========================
# Load CSS
# ==========================

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==========================
# Load API
# ==========================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="SkyBot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# ==========================
# Session State
# ==========================

if "messages" not in st.session_state:

    st.session_state.messages = []

    old_messages = load_messages()

    for role, message in old_messages:

        st.session_state.messages.append({
            "role": role,
            "content": message
        })
# ==========================
# Sidebar
# ==========================

with st.sidebar:

    st.title("🤖 SkyBot AI")
    st.write("Your Personal AI Assistant")

    if st.button("🗑️ New Chat"):
        clear_chat()
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Model")
    st.write("Gemini 3.6 Flash")

    st.divider()

    chat_text = ""

    for message in st.session_state.messages:
        role = "You" if message["role"] == "user" else "SkyBot"
        chat_text += f"{role}: {message['content']}\n\n"

    st.download_button(
        label="💾 Download Chat",
        data=chat_text,
        file_name="SkyBot_Chat.txt",
        mime="text/plain"
    )

    st.divider()

    st.write("Made with ❤️ using Python & Streamlit")

# ==========================
# Header
# ==========================

st.markdown("""
<div class="header">

<h1>🤖 SkyBot AI</h1>

<p>Your Personal AI Assistant powered by Gemini</p>

</div>
""", unsafe_allow_html=True)

# ==========================
# Welcome Screen
# ==========================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome">

        <h2>👋 Welcome to SkyBot AI</h2>

        <p>Your smart AI assistant powered by Google Gemini.</p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧠 Explain Artificial Intelligence"):
            st.session_state["quick_prompt"] = "Explain Artificial Intelligence"

        if st.button("💻 Write Python Code"):
            st.session_state["quick_prompt"] = "Write a Python Hello World program"

    with col2:
        if st.button("📚 Learn HTML"):
            st.session_state["quick_prompt"] = "Teach me HTML from basics"

        if st.button("🎯 Interview Questions"):
            st.session_state["quick_prompt"] = "Ask me Python interview questions"

# ==========================
# Show Previous Messages
# ==========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================
# Chat Input
# ==========================

prompt = st.chat_input("💬 Ask me anything...")

if "quick_prompt" in st.session_state:

    prompt = st.session_state["quick_prompt"]

    del st.session_state["quick_prompt"]

if prompt:

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    save_message("user", prompt)

    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):

        with st.spinner("🤖 SkyBot is thinking..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                answer = response.text

            except Exception as e:

                answer = f"❌ Error:\n\n{e}"

            st.markdown(answer)

    # Save AI Response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    save_message("assistant", answer)