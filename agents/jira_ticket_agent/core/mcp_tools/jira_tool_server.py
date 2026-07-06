
#from agents.jira_ticket_agent.core.mcp_tools.jira_api_service import JiraApiService
#from langchain_core.tools import tool
from mcp.server.fastmcp import FastMCP
from agents.jira_ticket_agent.core.services.jira_api_service import JiraApiService
from agents.shared.langchain_openai_model import retrieve_similar_data_from_vector_store

jira_api_service=JiraApiService()
mcp=FastMCP("Ticket-Support",port=8089)

@mcp.tool()
def create_jira_ticket_tool(summary,description):
    """
    Create JIRA Ticket in Jira Service Management

        Args:
            summary : Summary of the issue
            description: Issue Details


        Return:
            Json object contains below fields
            id : Jira ID
            key : Jira Key related to project in JIRA platform
            self : link

            example : {'id': '10077', 'key': 'MCP-12', 'self': 'https://vivekvishalnitjsr.atlassian.net/rest/api/3/issue/10077'}
    """
    response= jira_api_service.create_jira_ticket(summary=summary,description=description)
    print(response)
    return response

@mcp.tool()
def add_jira_comment_tool( key: str, comment: str ):
    """ Add comment in the jira for the key

        Args:
            key : Jira Key where comment will be add
            comment: Comment to be updated in the jira key
        Return:
            message : "Comment Added"
            browse : link

            example : {'message': 'Comment Added', 'browse': 'https://vivekvishalnitjsr.atlassian.net/browse/MCP-58'}
        """
    response = jira_api_service.add_jira_comment(key=key,comment=comment)
    print(response)
    return response
@mcp.tool()
def get_resolution_from_vector_store(query):
    print("RAG TOOL")
    """
    It is RAG based tool it fetches similar documents w.r.t query from vector store
    contains resolution from historical jira.

    :param query: Query is summary/description of Jira
    :return: string documents to used while call llm
    """
    doc =  retrieve_similar_data_from_vector_store(query)
    return doc
@mcp.tool()
def get_jira_description(key):

    """Get Jira by Key

                Args:
                    key : Jira to be fetched
                    e.g : "MCP-63"

                Return:
                    content and description

                    example : [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Users are facing an Internal Server Error when trying to log in. This issue needs to be investigated and resolved promptly.'}], 'attrs': {'localId': '69ded477f991'}}, {'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Please check ASAP'}], 'attrs': {'localId': '14126746eca5'}}]

    """
    doc =  jira_api_service.get_jira_by_key(key)
    return doc

def run_mcp_server():
    print("Jira MCP Server Starting")
    #mcp.run(transport="stdio")
    mcp.run(transport="streamable-http")
if __name__ == "__main__":
    run_mcp_server()

"""
k= get_jira_description("MCP-63")
print(k)
"""