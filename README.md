# langchain-quercle

Quercle web search, fetch, and extraction tools for [LangChain](https://python.langchain.com/).

## Installation

```bash
uv add langchain-quercle
# or
pip install langchain-quercle
```

## Setup

Set your API key as an environment variable:

```bash
export QUERCLE_API_KEY=qk_...
```

Get your API key at [quercle.dev](https://quercle.dev).

## Quick Start

```python
from quercle_langchain import QuercleSearchTool, QuercleFetchTool

search = QuercleSearchTool()
result = search.invoke("latest developments in AI agents")
print(result)
```

## Tools

| Tool | Description | Key Args |
|---|---|---|
| `QuercleSearchTool` | AI-synthesized web search with citations | `query`, `allowed_domains`, `blocked_domains` |
| `QuercleFetchTool` | Fetch a URL and analyze content with AI | `url`, `prompt` |
| `QuercleRawSearchTool` | Raw web search results (markdown/JSON) | `query`, `format`, `use_safeguard` |
| `QuercleRawFetchTool` | Raw URL content (markdown/HTML) | `url`, `format`, `use_safeguard` |
| `QuercleExtractTool` | Extract relevant content chunks from a URL | `url`, `query`, `format`, `use_safeguard` |

## Direct Tool Usage

### Sync

```python
from quercle_langchain import (
    QuercleSearchTool,
    QuercleFetchTool,
    QuercleRawSearchTool,
    QuercleRawFetchTool,
    QuercleExtractTool,
)

# AI-synthesized search
search = QuercleSearchTool()
result = search.invoke("best practices for building AI agents")
print(result)

# Search with domain filtering
result = search.invoke({
    "query": "Python documentation",
    "allowed_domains": ["docs.python.org"],
})

# Fetch and analyze a page with AI
fetch = QuercleFetchTool()
result = fetch.invoke({
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "prompt": "Summarize the key features of Python",
})
print(result)

# Raw search results
raw_search = QuercleRawSearchTool()
result = raw_search.invoke({"query": "Python tutorials", "format": "json"})
print(result)

# Raw URL content
raw_fetch = QuercleRawFetchTool()
result = raw_fetch.invoke({"url": "https://example.com", "use_safeguard": True})
print(result)

# Extract relevant content from a URL
extract = QuercleExtractTool()
result = extract.invoke({
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "query": "What are Python's main features?",
    "format": "json",
})
print(result)
```

### Async

```python
import asyncio
from quercle_langchain import (
    QuercleSearchTool,
    QuercleFetchTool,
    QuercleRawSearchTool,
    QuercleRawFetchTool,
    QuercleExtractTool,
)

async def main():
    # AI-synthesized search
    search = QuercleSearchTool()
    result = await search.ainvoke("latest AI agent frameworks")
    print(result)

    # Fetch and analyze with AI
    fetch = QuercleFetchTool()
    result = await fetch.ainvoke({
        "url": "https://en.wikipedia.org/wiki/TypeScript",
        "prompt": "What is TypeScript?",
    })
    print(result)

    # Raw search results
    raw_search = QuercleRawSearchTool()
    result = await raw_search.ainvoke({"query": "Python tutorials", "format": "json"})
    print(result)

    # Raw URL content
    raw_fetch = QuercleRawFetchTool()
    result = await raw_fetch.ainvoke({"url": "https://example.com"})
    print(result)

    # Extract relevant content
    extract = QuercleExtractTool()
    result = await extract.ainvoke({
        "url": "https://en.wikipedia.org/wiki/TypeScript",
        "query": "What is TypeScript used for?",
    })
    print(result)

asyncio.run(main())
```

### Custom API Key

```python
search = QuercleSearchTool(api_key="qk_...")
fetch = QuercleFetchTool(api_key="qk_...")
raw_search = QuercleRawSearchTool(api_key="qk_...")
raw_fetch = QuercleRawFetchTool(api_key="qk_...")
extract = QuercleExtractTool(api_key="qk_...")
```

## Agentic Usage

### With LangGraph ReAct Agent

```python
from quercle_langchain import (
    QuercleSearchTool,
    QuercleFetchTool,
    QuercleRawSearchTool,
    QuercleRawFetchTool,
    QuercleExtractTool,
)
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

model = ChatOpenAI(model="gpt-4o")
tools = [
    QuercleSearchTool(),
    QuercleFetchTool(),
    QuercleRawSearchTool(),
    QuercleRawFetchTool(),
    QuercleExtractTool(),
]

agent = create_react_agent(model, tools)

response = agent.invoke({
    "messages": [
        {"role": "user", "content": "Search for the latest AI news and summarize the top story"}
    ]
})

print(response["messages"][-1].content)
```

### Streaming

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Research WebAssembly trends"}]},
    stream_mode="values",
):
    print(chunk["messages"][-1].content)
```

### With Anthropic

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-20250514")
agent = create_react_agent(model, tools)
```

## API Reference

### QuercleSearchTool

AI-synthesized web search with citations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | `str` | Yes | The search query |
| `allowed_domains` | `list[str]` | No | Only include results from these domains |
| `blocked_domains` | `list[str]` | No | Exclude results from these domains |

### QuercleFetchTool

Fetch a URL and analyze its content with AI.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | `str` | Yes | The URL to fetch |
| `prompt` | `str` | Yes | Instructions for content analysis |

### QuercleRawSearchTool

Raw web search results without AI synthesis.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | `str` | Yes | The search query |
| `format` | `str` | No | Output format (e.g. `"json"`) |
| `use_safeguard` | `bool` | No | Enable prompt-injection detection |

### QuercleRawFetchTool

Raw URL content without AI processing.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | `str` | Yes | The URL to fetch |
| `format` | `str` | No | Output format (e.g. `"json"`) |
| `use_safeguard` | `bool` | No | Enable prompt-injection detection |

### QuercleExtractTool

Extract content chunks relevant to a query from a URL.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | `str` | Yes | The URL to fetch and extract from |
| `query` | `str` | Yes | What information to extract |
| `format` | `str` | No | Output format (e.g. `"json"`) |
| `use_safeguard` | `bool` | No | Enable prompt-injection detection |

## Configuration

All tools accept these constructor parameters:

| Parameter | Default | Description |
|---|---|---|
| `api_key` | `QUERCLE_API_KEY` env var | Your Quercle API key |
| `timeout` | `None` | Request timeout in seconds |

## License

MIT
