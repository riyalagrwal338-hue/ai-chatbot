import streamlit as st
import os
from google import genai

st.set_page_config(page_title="Mera AI Chatbot", page_icon="🤖")
st.title("🤖 Mera AI Chatbot")

# Fetch API Key safely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please configure GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if user_query := st.chat_input("Kuch bhi pucho..."):
    # Display user message
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Generate response from Gemini using fresh client instance every time
    try:
        client = genai.Client(api_key=api_key)
        
        with st.chat_message("assistant"):
            with st.spinner("Soch raha hoon..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_query
                )
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

  
