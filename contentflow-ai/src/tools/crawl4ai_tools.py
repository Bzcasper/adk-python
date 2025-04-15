"""Tools for web content extraction using crawl4ai.

This module provides tools for extracting content from websites using the
crawl4ai library. These tools can be used by the extraction agents to retrieve
content from various web sources.
"""

from typing import Dict, Optional, Any
from google.adk.tools import Tool
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import MarkdownExtractionStrategy
import logging


async def extract_web_content(url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Extract content from a web page using crawl4ai.

    Args:
        url (str): The URL of the web page to extract content from.
        selectors (Optional[Dict[str, str]]): Optional CSS selectors to extract specific content.
            Format: {'title': 'h1', 'content': 'article', ...}

    Returns:
        Dict[str, Any]: A dictionary containing the extracted content with metadata.
    """
    try:
        crawler = AsyncWebCrawler(
            extraction_strategy=MarkdownExtractionStrategy(),
            browser_config=BrowserConfig(headless=True)
        )
        run_config = CrawlerRunConfig(timeout=60)
        extraction_args = {"url": url}
        if selectors:
            extraction_args["selectors"] = selectors
        result = await crawler.extract(**extraction_args, run_config=run_config)
        content = result.get("content", "")
        title = result.get("title", "")
        metadata = result.get("metadata", {})
        metadata.update({
            "source": url
        })
        return {
            "url": url,
            "title": title,
            "content": content,
            "metadata": metadata
        }
    except Exception as e:
        logging.exception(f"Failed to extract web content from {url}")
        return {
            "url": url,
            "title": None,
            "content": None,
            "metadata": {"source": url, "error": str(e)}
        }


async def extract_article_content(url: str) -> Dict[str, Any]:
    """
    Extract article content from a web page using crawl4ai.

    This function is specialized for article extraction, focusing on
    title, author, publication date, and main content.

    Args:
        url (str): The URL of the article to extract content from.

    Returns:
        Dict[str, Any]: A dictionary containing the extracted article content with metadata.
    """
    try:
        crawler = AsyncWebCrawler(
            extraction_strategy=MarkdownExtractionStrategy(article_mode=True),
            browser_config=BrowserConfig(headless=True)
        )
        run_config = CrawlerRunConfig(timeout=60)
        result = await crawler.extract(url=url, run_config=run_config)
        title = result.get("title", "")
        author = result.get("author", None)
        published_date = result.get("published_date", None)
        content = result.get("content", "")
        images = result.get("images", [])
        metadata = result.get("metadata", {})
        metadata.update({"source": url})
        return {
            "url": url,
            "title": title,
            "author": author,
            "published_date": published_date,
            "content": content,
            "images": images,
            "metadata": metadata
        }
    except Exception as e:
        logging.exception(f"Failed to extract article content from {url}")
        return {
            "url": url,
            "title": None,
            "author": None,
            "published_date": None,
            "content": None,
            "images": [],
            "metadata": {"source": url, "error": str(e)}
        }


# Create ADK tools for web content extraction
web_content_extraction_tool = Tool(
    name="extract_web_content",
    description="Extracts content from a web page using crawl4ai",
    function=extract_web_content
)

article_extraction_tool = Tool(
    name="extract_article_content",
    description="Extracts article content from a web page using crawl4ai",
    function=extract_article_content
)
