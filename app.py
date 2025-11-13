import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

load_dotenv()


st.title("langchain-streamlit-app")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        chat = ChatOpenAI(
            model=os.getenv("OPENAI_API_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_API_TEMPERATURE", 0.5)),
        )
        # 過去のメッセージ履歴を LangChain フォーマットに変換
        message_history = []
        for msg in st.session_state.messages:  # 最後の新しいメッセージを除外
            if msg["role"] == "user":
                message_history.append(HumanMessage(content=msg["content"]))
            else:
                message_history.append(AIMessage(content=msg["content"]))
        
        response = chat(messages=message_history)
        st.markdown(response.content)
    st.session_state.messages.append({"role": "assistant", "content": response.content})