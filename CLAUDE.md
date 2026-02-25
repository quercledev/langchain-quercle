# CLAUDE.md - Quercle LangChain Integration

## Project Overview

Python package integrating Quercle web tools with LangChain agents. Provides 5 tools: `QuercleSearchTool`, `QuercleFetchTool`, `QuercleRawSearchTool`, `QuercleRawFetchTool`, and `QuercleExtractTool`.

## Development Guidelines

**IMPORTANT:**
- Always use the **latest stable versions** of all dependencies
- Use **`uv`** for Python package management (NOT pip)
- Use modern Python patterns and type hints
- Check PyPI for current versions before specifying dependencies

## Quercle API

### Authentication
- Header: `Authorization: Bearer qk_...`
- Env var: `QUERCLE_API_KEY`

### Endpoints

**POST https://api.quercle.dev/v1/search** - AI-synthesized search with citations
```json
{"query": "...", "allowed_domains": ["*.edu"], "blocked_domains": ["spam.com"]}
```

**POST https://api.quercle.dev/v1/fetch** - Fetch URL and analyze with AI
```json
{"url": "https://...", "prompt": "Summarize this page"}
```

**POST https://api.quercle.dev/v1/raw_search** - Raw search results (markdown/JSON)
```json
{"query": "...", "format": "markdown", "use_safeguard": true}
```

**POST https://api.quercle.dev/v1/raw_fetch** - Raw URL content (markdown/HTML)
```json
{"url": "https://...", "format": "markdown", "use_safeguard": true}
```

**POST https://api.quercle.dev/v1/extract** - Extract relevant chunks from URL
```json
{"url": "https://...", "query": "What are the main features?", "format": "markdown", "use_safeguard": true}
```

## Package Structure

```
quercle_langchain/
├── __init__.py          # Exports all 5 tools
├── tools.py             # LangChain Tool implementations (uses quercle SDK)
└── py.typed             # PEP 561 marker
tests/
└── test_tools.py
pyproject.toml
README.md
LICENSE                  # MIT
```

## Tools

All tools extend `langchain_core.tools.BaseTool`. Descriptions and parameter metadata come from `tool_metadata` (imported from the `quercle` SDK).

### QuercleSearchTool
- Name: `search`
- Description: `tool_metadata["search"]["description"]`
- Args: `query`, `allowed_domains`, `blocked_domains`

### QuercleFetchTool
- Name: `fetch`
- Description: `tool_metadata["fetch"]["description"]`
- Args: `url`, `prompt`

### QuercleRawSearchTool
- Name: `raw_search`
- Description: `tool_metadata["raw_search"]["description"]`
- Args: `query`, `format`, `use_safeguard`

### QuercleRawFetchTool
- Name: `raw_fetch`
- Description: `tool_metadata["raw_fetch"]["description"]`
- Args: `url`, `format`, `use_safeguard`

### QuercleExtractTool
- Name: `extract`
- Description: `tool_metadata["extract"]["description"]`
- Args: `url`, `query`, `format`, `use_safeguard`

## Commands

```bash
uv sync                    # Install deps
uv run pytest             # Run tests
uv run ruff check .       # Lint
uv build                  # Build package
uv publish                # Publish to PyPI
```

## Dependencies

- Python 3.10+
- quercle >= 1.0.0 (Quercle Python SDK)
- langchain-core >= 0.2.0
- pydantic >= 2.0

## Usage Example

```python
from quercle_langchain import (
    QuercleSearchTool,
    QuercleFetchTool,
    QuercleRawSearchTool,
    QuercleRawFetchTool,
    QuercleExtractTool,
)

# Initialize (uses QUERCLE_API_KEY env var, or pass api_key="qk_...")
search = QuercleSearchTool()
fetch = QuercleFetchTool()
raw_search = QuercleRawSearchTool()
raw_fetch = QuercleRawFetchTool()
extract = QuercleExtractTool()

# Use with LangChain agent
from langchain_core.tools import tool
tools = [search, fetch, raw_search, raw_fetch, extract]
# Pass tools to your agent or chain, e.g.:
# agent = create_tool_calling_agent(llm, tools, prompt)

# Direct usage
result = search.invoke({"query": "What is TypeScript?"})
result = fetch.invoke({"url": "https://example.com", "prompt": "Summarize"})
result = raw_fetch.invoke({"url": "https://example.com"})
result = extract.invoke({"url": "https://example.com", "query": "Main features"})
```

### SDK imports (in tools.py)

```python
from quercle import QuercleClient, AsyncQuercleClient, tool_metadata
```

## Publishing

- Package name on PyPI: `langchain-quercle`
- Use trusted publishing with GitHub Actions OIDC
