import os
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain.globals import set_debug, set_verbose

# set_debug(True)
# set_verbose(True)

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

mcp_servers = [
    {
        "name": "google_maps",
        "params": StdioServerParameters(
            command="docker",
            args=[
                "run",
                "-i",
                "--rm",
                "-e",
                "GOOGLE_MAPS_API_KEY",
                "mcp/google-maps"
            ],
            env={
                "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
            }
        )
    },
    # {
    #     "name": "custom_mcp_server",
    #     "params": StdioServerParameters(
    #         command="python",
    #         args=["custom_mcp_server.py"]
    #     )
    # }
]


async def connect_to_server(exit_stack, server_config):
    """Connect to a single MCP server and load its tools"""
    name = server_config["name"]
    server_params = server_config["params"]

    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))

    await session.initialize()

    tools = await load_mcp_tools(session)
    print(f"\nConnected to MCP server {name} with tools:", [
        tool.name for tool in tools])

    return tools


async def run_multi_server_agent(exit_stack):
    # Connect to all servers
    all_tools = []
    for server in mcp_servers:
        tools = await connect_to_server(exit_stack, server)
        all_tools.extend(tools)

    # for tool in all_tools:
        # print(tool)

    print(
        f"Connected successfully to {len(mcp_servers)} servers with a total of {len(tools)} tools!")

    return all_tools


async def process_query(query: str, tools) -> str:
    # AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY and OPENAI_API_VERSION must be set in .env file,
    # and will be automatically read by the AzureOpenAI class.
    llmModel = AzureChatOpenAI(
        azure_deployment="gpt-4o-2024-11-20-128k-no-filter",
        api_version="2024-12-01-preview",
    )

    agent = create_react_agent(
        llmModel,
        tools
    )

    # Runs the agent with a query that might use multiple MCP server tools
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    return result["messages"][-1].content


async def main():
    exit_stack = AsyncExitStack()
    tools = await run_multi_server_agent(exit_stack)
    response = await process_query(
        "How long does it take to drive from Oslo to Stockholm? And how much elevation is it along the route?",
        tools
    )
    print(response)
    await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(main())
