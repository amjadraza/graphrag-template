
import os
import sys
# sys.path.append(".")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.global_search import main as global_main
import streamlit as st
import asyncio

if __name__ == "__main__":
    st.set_page_config(
        page_title="graphrag",
        page_icon="🧰",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
        'Get Help': 'https://www.datafyassociates.com/',
        'Report a bug': "https://www.datafyassociates.com/",
        'About': "# This is sample app to interact with graphrag"
        })
    st.title("💬 Chatbot: Interact with GraphRag")
    st.caption("🚀 AI Companion to help you quickly converse with data.")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "This your AI Companion for graphrag, ASK me?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        result = asyncio.run(global_main(prompt))
        msg =  result.response
        # msg = response[2].content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)