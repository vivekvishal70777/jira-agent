
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

from agents.shared.prompt import ai_assistant_role
import streamlit as st

load_dotenv()
OPENAI_API_KEY = os.getenv("")

llm = ChatOpenAI(model = "gpt-4.1-mini",api_key= OPENAI_API_KEY)

_tools = None
_agent = None

@st.cache_resource
def get_in_memory_saver():
    return InMemorySaver()

@st.cache_resource
def get_mcp_client():
    mcp_session = MultiServerMCPClient({
            "jira": {
                "command" : "python",
                #"args" : ["./agents/jira_ticket_agent/core/mcp_tools/jira_tool_server.py"],
                "url": "http://localhost:8089/mcp",
                "transport": "http", }}
        )
    return mcp_session



async def create_llm_agent(_llm_model):
    global _agent, _tools

    if _agent is not None:
        return _agent

    client = get_mcp_client()

    _tools = await client.get_tools()

    return create_agent(model=_llm_model,
                        tools=_tools,
                        system_prompt= f"""role": "AI-ASSISTANT", "content": {ai_assistant_role}, "tools" : {_tools}""",
                        checkpointer=get_in_memory_saver()
        )



async def invoke_llm(prompt,thread_id):

    agent = await create_llm_agent(llm)
    response = await agent.ainvoke(
        {
            "messages":[
                {"role": "user", "content": prompt}
            ]
        },
        config= {
        "configurable" : {
            "thread_id": thread_id
        }
    })
    print(response["messages"][-1].content)
    return (response["messages"][-1].content)




#if __name__ == "__main__":
 # asyncio.run(main(prompt))
#" GET JIRA description from MCP-63 and search its resolution and then update the comment in same jira"

