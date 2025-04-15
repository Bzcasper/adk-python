"""
Unit tests for crawl4ai_tools web extraction functions.
"""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock

try:
    from src.tools import crawl4ai_tools
except ImportError:
    try:
        from ...src.tools import crawl4ai_tools
    except ImportError:
        import importlib.util, os, sys
        tool_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src/tools/crawl4ai_tools.py'))
        spec = importlib.util.spec_from_file_location('crawl4ai_tools', tool_path)
        crawl4ai_tools = importlib.util.module_from_spec(spec)
        sys.modules['crawl4ai_tools'] = crawl4ai_tools
        spec.loader.exec_module(crawl4ai_tools)

@pytest.mark.asyncio
async def test_extract_web_content_expected(monkeypatch):
    """Test extract_web_content returns structured content for a valid URL."""
    async def mock_extract(**kwargs):
        return {
            "title": "Test Title",
            "content": "Test Content",
            "metadata": {"word_count": 42}
        }
    monkeypatch.setattr(crawl4ai_tools.AsyncWebCrawler, "extract", mock_extract)
    url = "https://example.com"
    result = await crawl4ai_tools.extract_web_content(url, selectors={"title": "h1"})
    assert result["url"] == url
    assert result["title"] == "Test Title"
    assert result["content"] == "Test Content"
    assert "metadata" in result
    assert result["metadata"]["word_count"] == 42
    assert result["metadata"]["source"] == url

@pytest.mark.asyncio
async def test_extract_web_content_invalid_url(monkeypatch):
    """Test extract_web_content handles invalid URL edge case."""
    async def mock_extract(**kwargs):
        raise ValueError("Invalid URL")
    monkeypatch.setattr(crawl4ai_tools.AsyncWebCrawler, "extract", mock_extract)
    url = "not-a-valid-url"
    result = await crawl4ai_tools.extract_web_content(url)
    assert result["url"] == url
    assert result["title"] is None
    assert result["content"] is None
    assert "error" in result["metadata"]

@pytest.mark.asyncio
async def test_extract_article_content_failure(monkeypatch):
    """Test extract_article_content returns error metadata on crawl4ai failure."""
    async def mock_extract(**kwargs):
        raise RuntimeError("crawl4ai crashed")
    monkeypatch.setattr(crawl4ai_tools.AsyncWebCrawler, "extract", mock_extract)
    url = "https://example.com/article"
    result = await crawl4ai_tools.extract_article_content(url)
    assert result["url"] == url
    assert result["title"] is None
    assert result["author"] is None
    assert result["content"] is None
    assert "error" in result["metadata"]
