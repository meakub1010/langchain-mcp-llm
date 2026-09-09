### READ ME


```bash
    cd /Volumes/Ext-Drive/Development
    mkdir -p langchain-mcp-llm/docker langchain-mcp-llm/app langchain-mcp-llm/mcp_server langchain-mcp-llm/tests
    mkdir -p langchain-mcp-llm-data/postgres langchain-mcp-llm-data/redis
    cd langchain-mcp-llm
    git init

    uv init --python 3.12
```

### Docker commands
```bash
    docker compose ps
    docker compose logs
    docker context ls
```

### accessing postgres
```text
Open any instance of pgadmin and register new server

Open localhost:5050, right-click Servers → Register → Server.
General tab: Name it langchain-mcp-llm.
Connection tab:
Host: host.docker.internal — not localhost. This matters: pgAdmin itself runs inside its own container, so localhost from its point of view means "inside the pgAdmin container," not your Mac. host.docker.internal is Docker Desktop's special hostname for "the actual Mac host," which is what lets pgAdmin reach a container it's not directly linked to.
Port: 5433 (the host-mapped port from the compose file — not 5432, since that's pocket-attorney-rag's port).
Maintenance database: 
Username / Password: 
```

### initial packages 

```bash
  uv add langchain langchain-anthropic langchain-openai python-dotenv
```
### Create read only role for llm to use so it can't delete or drop anything
scripts in schema sql file run in query tool for postgres

### langchain-mcp-adapters 
langchain-mcp-adapters is an official LangChain library (Python, with a JS/TS version too) whose whole job is to act as a bridge between MCP servers and LangChain/LangGraph agents — it converts MCP tools into the tool format LangChain agents expect, so you don't have to write that glue code yourself.

```bash
    uv add mcp langchain-mcp-adapters "psycopg[binary]"
```
* **mcp** — the official Model Context Protocol SDK. This is what mcp_server/server.py will use to define tools and run the stdio server.
* **langchain-mcp-adapters** — the bridge library; it lets a LangChain agent connect to an MCP server and use its tools as if they were native LangChain tools. This is the piece that makes "MCP server" and "LangChain agent" actually talk to each other.
* **psycopg[binary]** — the Postgres driver mcp_server/db.py will use to actually run SQL against your database. The [binary] extra pulls in prebuilt binaries so you don't need Postgres's C headers installed locally to get it working.


### MCP Model Context Protocol
    standard for exposing tools/data to LLMs

**What it actually does**
* Converts MCP tools into LangChain- & LangGraph-compatible tools
* Enables interaction with tools across multiple MCP servers
* Seamlessly integrates the hundreds of tool servers already published into LangGraph Agents 


### Add langgraph
```bash
uv add langgraph
```


### add sentence transformer for embedding, there is alternative using openai, need api key
```bash
uv add sentence-transformers
```

### add dependency for chunking the text for better embedding
```bash
uv add langchain-text-splitters pypdf
```
