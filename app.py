import asyncio
import streamlit as st
import uuid
from agents.jira_ticket_agent.agent import invoke_llm

async def main(prompt,chat_history):
    llm_response = await invoke_llm(prompt,chat_history)
    return llm_response

st.title("JIRA SUPPORT")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "CHAT-1"
if "messages" not in st.session_state:
    st.session_state.messages =[]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt=st.chat_input("Provide your request")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Assistant working on your request, Please wait"):
            result = asyncio.run(main(prompt,st.session_state.thread_id))
            st.write(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
#if __name__ == "__main__":
 # asyncio.run(main(prompt))