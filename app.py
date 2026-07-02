import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("🤖 Mera AI Chatbot")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Please configure GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

config = types.GenerateContentConfig(
    system_instruction="You are a helpful AI assistant. Always reply in friendly Hinglish.",
    temperature=0.7
)

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-3.5-flash", config=config)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

user_input = st.chat_input("Kuch bhi pucho...")
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})
    
    response = st.session_state.chat.send_message(user_input)
    
    st.chat_message("assistant").write(response.text)
    st.session_state.messages.append({"role": "assistant", "text": response.text})
  
