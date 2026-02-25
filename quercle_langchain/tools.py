"""LangChain tools for Quercle web search and URL fetching."""

import json
from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from quercle import (
    AsyncQuercleClient,
    QuercleClient,
    tool_metadata,
)


class SearchInput(BaseModel):
    """Input schema for the Quercle search tool."""

    query: str = Field(description=tool_metadata["search"]["parameters"]["query"])
    allowed_domains: Optional[list[str]] = Field(
        default=None,
        description=tool_metadata["search"]["parameters"]["allowed_domains"],
    )
    blocked_domains: Optional[list[str]] = Field(
        default=None,
        description=tool_metadata["search"]["parameters"]["blocked_domains"],
    )


class FetchInput(BaseModel):
    """Input schema for the Quercle fetch tool."""

    url: str = Field(description=tool_metadata["fetch"]["parameters"]["url"])
    prompt: str = Field(description=tool_metadata["fetch"]["parameters"]["prompt"])


class RawFetchInput(BaseModel):
    """Input schema for the Quercle raw fetch tool."""

    url: str = Field(description=tool_metadata["raw_fetch"]["parameters"]["url"])
    format: Optional[str] = Field(
        default=None,
        description=tool_metadata["raw_fetch"]["parameters"]["format"],
    )
    use_safeguard: Optional[bool] = Field(
        default=None,
        description=tool_metadata["raw_fetch"]["parameters"]["use_safeguard"],
    )


class RawSearchInput(BaseModel):
    """Input schema for the Quercle raw search tool."""

    query: str = Field(description=tool_metadata["raw_search"]["parameters"]["query"])
    format: Optional[str] = Field(
        default=None,
        description=tool_metadata["raw_search"]["parameters"]["format"],
    )
    use_safeguard: Optional[bool] = Field(
        default=None,
        description=tool_metadata["raw_search"]["parameters"]["use_safeguard"],
    )


class ExtractInput(BaseModel):
    """Input schema for the Quercle extract tool."""

    url: str = Field(description=tool_metadata["extract"]["parameters"]["url"])
    query: str = Field(description=tool_metadata["extract"]["parameters"]["query"])
    format: Optional[str] = Field(
        default=None,
        description=tool_metadata["extract"]["parameters"]["format"],
    )
    use_safeguard: Optional[bool] = Field(
        default=None,
        description=tool_metadata["extract"]["parameters"]["use_safeguard"],
    )


class QuercleSearchTool(BaseTool):
    """Tool for searching the web and getting AI-synthesized answers with citations.

    This tool uses the Quercle API to perform web searches and return
    AI-synthesized answers with source citations.

    Example:
        >>> tool = QuercleSearchTool()
        >>> result = tool.invoke({"query": "What is TypeScript?"})
    """

    name: str = "search"
    description: str = tool_metadata["search"]["description"]
    args_schema: Type[BaseModel] = SearchInput

    api_key: Optional[str] = Field(
        default=None,
        description="Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.",
    )
    timeout: Optional[float] = Field(
        default=None,
        description="Request timeout in seconds.",
    )

    _sync_client: Optional[QuercleClient] = PrivateAttr(default=None)
    _async_client: Optional[AsyncQuercleClient] = PrivateAttr(default=None)

    def _get_sync_client(self) -> QuercleClient:
        """Get or create the synchronous Quercle client."""
        if self._sync_client is None:
            self._sync_client = QuercleClient(
                api_key=self.api_key,
            )
        return self._sync_client

    def _get_async_client(self) -> AsyncQuercleClient:
        """Get or create the asynchronous Quercle client."""
        if self._async_client is None:
            self._async_client = AsyncQuercleClient(
                api_key=self.api_key,
            )
        return self._async_client

    def _run(
        self,
        query: str,
        allowed_domains: Optional[list[str]] = None,
        blocked_domains: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute a synchronous web search.

        Args:
            query: The search query.
            allowed_domains: Optional list of domains to include.
            blocked_domains: Optional list of domains to exclude.
            run_manager: Optional callback manager.

        Returns:
            AI-synthesized answer with citations.
        """
        return self._get_sync_client().search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=self.timeout,
        ).result

    async def _arun(
        self,
        query: str,
        allowed_domains: Optional[list[str]] = None,
        blocked_domains: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Execute an asynchronous web search.

        Args:
            query: The search query.
            allowed_domains: Optional list of domains to include.
            blocked_domains: Optional list of domains to exclude.
            run_manager: Optional callback manager.

        Returns:
            AI-synthesized answer with citations.
        """
        return (await self._get_async_client().search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=self.timeout,
        )).result


class QuercleFetchTool(BaseTool):
    """Tool for fetching a URL and analyzing its content with AI.

    This tool uses the Quercle API to fetch web pages and analyze
    their content based on a provided prompt.

    Example:
        >>> tool = QuercleFetchTool()
        >>> result = tool.invoke({
        ...     "url": "https://example.com",
        ...     "prompt": "Summarize the main points"
        ... })
    """

    name: str = "fetch"
    description: str = tool_metadata["fetch"]["description"]
    args_schema: Type[BaseModel] = FetchInput

    api_key: Optional[str] = Field(
        default=None,
        description="Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.",
    )
    timeout: Optional[float] = Field(
        default=None,
        description="Request timeout in seconds.",
    )

    _sync_client: Optional[QuercleClient] = PrivateAttr(default=None)
    _async_client: Optional[AsyncQuercleClient] = PrivateAttr(default=None)

    def _get_sync_client(self) -> QuercleClient:
        """Get or create the synchronous Quercle client."""
        if self._sync_client is None:
            self._sync_client = QuercleClient(
                api_key=self.api_key,
            )
        return self._sync_client

    def _get_async_client(self) -> AsyncQuercleClient:
        """Get or create the asynchronous Quercle client."""
        if self._async_client is None:
            self._async_client = AsyncQuercleClient(
                api_key=self.api_key,
            )
        return self._async_client

    def _run(
        self,
        url: str,
        prompt: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute a synchronous URL fetch and analysis.

        Args:
            url: The URL to fetch.
            prompt: Instructions for content analysis.
            run_manager: Optional callback manager.

        Returns:
            AI-processed content based on the prompt.
        """
        return self._get_sync_client().fetch(url=url, prompt=prompt, timeout=self.timeout).result

    async def _arun(
        self,
        url: str,
        prompt: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Execute an asynchronous URL fetch and analysis.

        Args:
            url: The URL to fetch.
            prompt: Instructions for content analysis.
            run_manager: Optional callback manager.

        Returns:
            AI-processed content based on the prompt.
        """
        return (await self._get_async_client().fetch(
            url=url, prompt=prompt, timeout=self.timeout
        )).result


class QuercleRawFetchTool(BaseTool):
    """Tool for fetching a URL and returning raw markdown or HTML content.

    This tool uses the Quercle API to fetch web pages and return their
    content in raw markdown or HTML format.

    Example:
        >>> tool = QuercleRawFetchTool()
        >>> result = tool.invoke({"url": "https://example.com"})
    """

    name: str = "raw_fetch"
    description: str = tool_metadata["raw_fetch"]["description"]
    args_schema: Type[BaseModel] = RawFetchInput

    api_key: Optional[str] = Field(
        default=None,
        description="Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.",
    )
    timeout: Optional[float] = Field(
        default=None,
        description="Request timeout in seconds.",
    )

    _sync_client: Optional[QuercleClient] = PrivateAttr(default=None)
    _async_client: Optional[AsyncQuercleClient] = PrivateAttr(default=None)

    def _get_sync_client(self) -> QuercleClient:
        """Get or create the synchronous Quercle client."""
        if self._sync_client is None:
            self._sync_client = QuercleClient(
                api_key=self.api_key,
            )
        return self._sync_client

    def _get_async_client(self) -> AsyncQuercleClient:
        """Get or create the asynchronous Quercle client."""
        if self._async_client is None:
            self._async_client = AsyncQuercleClient(
                api_key=self.api_key,
            )
        return self._async_client

    def _run(
        self,
        url: str,
        format: Optional[str] = None,
        use_safeguard: Optional[bool] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute a synchronous raw URL fetch.

        Args:
            url: The URL to fetch.
            format: Output format for fetched content.
            use_safeguard: Enable prompt-injection detection.
            run_manager: Optional callback manager.

        Returns:
            Raw markdown or HTML content from the URL.
        """
        response = self._get_sync_client().raw_fetch(
            url, format=format, use_safeguard=use_safeguard, timeout=self.timeout
        )
        result = response.result
        return result if isinstance(result, str) else json.dumps(result)

    async def _arun(
        self,
        url: str,
        format: Optional[str] = None,
        use_safeguard: Optional[bool] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Execute an asynchronous raw URL fetch.

        Args:
            url: The URL to fetch.
            format: Output format for fetched content.
            use_safeguard: Enable prompt-injection detection.
            run_manager: Optional callback manager.

        Returns:
            Raw markdown or HTML content from the URL.
        """
        response = await self._get_async_client().raw_fetch(
            url, format=format, use_safeguard=use_safeguard, timeout=self.timeout
        )
        result = response.result
        return result if isinstance(result, str) else json.dumps(result)


class QuercleRawSearchTool(BaseTool):
    """Tool for running a web search and returning raw results.

    This tool uses the Quercle API to perform web searches and return
    raw search results in markdown or JSON format.

    Example:
        >>> tool = QuercleRawSearchTool()
        >>> result = tool.invoke({"query": "What is TypeScript?"})
    """

    name: str = "raw_search"
    description: str = tool_metadata["raw_search"]["description"]
    args_schema: Type[BaseModel] = RawSearchInput

    api_key: Optional[str] = Field(
        default=None,
        description="Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.",
    )
    timeout: Optional[float] = Field(
        default=None,
        description="Request timeout in seconds.",
    )

    _sync_client: Optional[QuercleClient] = PrivateAttr(default=None)
    _async_client: Optional[AsyncQuercleClient] = PrivateAttr(default=None)

    def _get_sync_client(self) -> QuercleClient:
        """Get or create the synchronous Quercle client."""
        if self._sync_client is None:
            self._sync_client = QuercleClient(
                api_key=self.api_key,
            )
        return self._sync_client

    def _get_async_client(self) -> AsyncQuercleClient:
        """Get or create the asynchronous Quercle client."""
        if self._async_client is None:
            self._async_client = AsyncQuercleClient(
                api_key=self.api_key,
            )
        return self._async_client

    def _run(
        self,
        query: str,
        format: Optional[str] = None,
        use_safeguard: Optional[bool] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute a synchronous raw web search.

        Args:
            query: The search query.
            format: Output format for search results.
            use_safeguard: Enable prompt-injection detection.
            run_manager: Optional callback manager.

        Returns:
            Raw search results.
        """
        response = self._get_sync_client().raw_search(
            query, format=format, use_safeguard=use_safeguard, timeout=self.timeout
        )
        result = response.result
        return result if isinstance(result, str) else json.dumps(result)

    async def _arun(
        self,
        query: str,
        format: Optional[str] = None,
        use_safeguard: Optional[bool] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Execute an asynchronous raw web search.

        Args:
            query: The search query.
            format: Output format for search results.
            use_safeguard: Enable prompt-injection detection.
            run_manager: Optional callback manager.

        Returns:
            Raw search results.
        """
        response = await self._get_async_client().raw_search(
            query, format=format, use_safeguard=use_safeguard, timeout=self.timeout
        )
        result = response.result
        return result if isinstance(result, str) else json.dumps(result)


class QuercleExtractTool(BaseTool):
    """Tool for fetching a URL and extracting chunks relevant to a query.

    This tool uses the Quercle API to fetch web pages and return
    content chunks that are relevant to the provided query.

    Example:
        >>> tool = QuercleExtractTool()
        >>> result = tool.invoke({
        ...     "url": "https://example.com",
        ...     "query": "What are the main features?"
        ... })
    """

    name: str = "extract"
    description: str = tool_metadata["extract"]["description"]
    args_schema: Type[BaseModel] = ExtractInput

    api_key: Optional[str] = Field(
        default=None,
        description="Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.",
    )
    timeout: Optional[float] = Field(
        default=None,
        description="Request timeout in seconds.",
    )

    _sync_client: Optional[QuercleClient] = PrivateAttr(default=None)
    _async_client: Optional[AsyncQuercleClient] = PrivateAttr(default=None)

    def _get_sync_client(self) -> QuercleClient:
        """Get or create the synchronous Quercle client."""
        if self._sync_client is None:
            self._sync_client = QuercleClient(
                api_key=self.api_key,
            )
        return self._sync_client

    def _get_async_client(self) -> AsyncQuercleClient:
        """Get or create the asynchronous Quercle client."""
        if self._async_client is None:
            self._async_client = AsyncQuercleClient(
                api_key=self.api_key,
            )
        return self._async_client

    def _run(
        self,
        url: str,
        query: str,
        format: Optional[str] = None,
        use_safeguard: Optional[bool] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute a synchronous URL fetch and content extraction.

        Args:
            url: The URL to fetch and extract from.
            query: What information to extract from the page.
            format: Output format for extracted chunks.
            use_safeguard: Enable prompt-injection detection.
            run_manager: Optional callback manager.

        Returns:
            Extracted content chunks relevant to the query.
        """
        response = self._get_sync_client().extract(
            url, query, format=format, use_safeguard=use_safeguard, timeout=self.timeout
        )
        result = response.result
        return result if isinstance(result, str) else json.dumps(result)

    async def _arun(
        self,
        url: str,
        query: str,
        format: Optional[str] = None,
        use_safeguard: Optional[bool] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Execute an asynchronous URL fetch and content extraction.

        Args:
            url: The URL to fetch and extract from.
            query: What information to extract from the page.
            format: Output format for extracted chunks.
            use_safeguard: Enable prompt-injection detection.
            run_manager: Optional callback manager.

        Returns:
            Extracted content chunks relevant to the query.
        """
        response = await self._get_async_client().extract(
            url, query, format=format, use_safeguard=use_safeguard, timeout=self.timeout
        )
        result = response.result
        return result if isinstance(result, str) else json.dumps(result)
