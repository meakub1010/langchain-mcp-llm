# build langchain agent that will connect to mcp server as client

import asyncio
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

from app.model_factory import get_chat_model

MCP_SERVERS = {
    "langchain-mcp-llm": {
        "command": "uv",
        "args": ["run","python", "-m", "mcp_server.server"],
        "transport": "stdio",
    }
}

async def ask(question: str) -> str:
    agent = build_agent()
    result = await agent.ainvoke({"messages": [("user", question)]})
    return result["messages"][-1].content

async def build_agent():
    client = MultiServerMCPClient(MCP_SERVERS)
    tools = await client.get_tools()
    return create_agent(get_chat_model(), tools)

async def chat():
    agent = await build_agent()
    print("Connected. Ask a question (type 'exit' to quit). \n")
    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        result = await agent.ainvoke({"messages": [("user", question)]})
        print(result["messages"][-1].content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(asyncio.run(ask(sys.argv[1])))
    else:
        asyncio.run(chat())


# quick test run using this command
# uv run python -m app.agent "How many orders were shipped in total?"
