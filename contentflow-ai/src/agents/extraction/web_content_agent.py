"""Web content extraction agent for ContentFlow AI.

This module defines the WebContentAgent, which is responsible for extracting content
from websites using crawl4ai. It leverages Google's ADK to create an intelligent
agent that can extract, clean, and structure web content.
"""

from typing import Dict, List, Optional, Any
from google.adk.agents import Agent
from google.genai import types

from ...tools.crawl4ai_tools import web_content_extraction_tool, article_extraction_tool


class WebContentAgent:
    """Agent for extracting content from websites.
    
    This agent uses crawl4ai to extract content from websites and structure it
    for further processing. It can extract general web content or specialized
    content like articles.
    """
    
    def __init__(self, model: str = "gemini-2.0-flash"):
        """
        Initialize the WebContentAgent.
        
        Args:
            model: The model to use for the agent (default: gemini-2.0-flash).
        """
        self.agent = Agent(
            name="web_content_extractor",
            model=model,
            instruction="""
            You are a web content extraction specialist. Your task is to extract content
            from websites and structure it for further processing. Follow these guidelines:
            
            1. Extract the main content from the webpage, ignoring navigation, ads, and other irrelevant elements
            2. Identify the title, author, publication date, and other metadata when available
            3. Preserve the structure of the content, including headings, paragraphs, and lists
            4. Extract relevant images and their captions
            5. Clean the content by removing any noise or irrelevant information
            
            Use the provided tools to extract content from websites and return it in a structured format.
            """,
            description="Agent that extracts content from websites using crawl4ai",
            tools=[web_content_extraction_tool, article_extraction_tool]
        )
    
    async def extract_web_content(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Extract content from a web page.
        
        Args:
            url: The URL of the web page to extract content from.
            selectors: Optional CSS selectors to extract specific content.
                Format: {'title': 'h1', 'content': 'article', ...}
                
        Returns:
            A dictionary containing the extracted content with metadata.
        """
        response = await self.agent.generate_content_async(
            types.Content(
                parts=[
                    types.Part.from_text(
                        f"Extract content from this URL: {url}\n"
                        f"Selectors: {selectors if selectors else 'Use default selectors'}"
                    )
                ]
            )
        )
        
        # The agent will use the web_content_extraction_tool to extract the content
        # and return it in a structured format
        
        # For now, we'll return a placeholder result
        # In a real implementation, we would parse the agent's response
        return {
            "url": url,
            "title": "Sample Title",
            "content": "Sample content extracted from the web page.",
            "metadata": {
                "source": url,
                "extraction_time": "2025-04-15T01:00:00Z",
                "word_count": 100,
            }
        }
    
    async def extract_article(self, url: str) -> Dict[str, Any]:
        """
        Extract article content from a web page.
        
        This method is specialized for article extraction, focusing on
        title, author, publication date, and main content.
        
        Args:
            url: The URL of the article to extract content from.
            
        Returns:
            A dictionary containing the extracted article content with metadata.
        """
        response = await self.agent.generate_content_async(
            types.Content(
                parts=[
                    types.Part.from_text(
                        f"Extract article content from this URL: {url}\n"
                        f"Focus on extracting the title, author, publication date, and main content."
                    )
                ]
            )
        )
        
        # The agent will use the article_extraction_tool to extract the article
        # and return it in a structured format
        
        # For now, we'll return a placeholder result
        # In a real implementation, we would parse the agent's response
        return {
            "url": url,
            "title": "Sample Article Title",
            "author": "John Doe",
            "published_date": "2025-04-10",
            "content": "Sample article content extracted from the web page.",
            "images": ["https://example.com/image1.jpg"],
            "metadata": {
                "source": url,
                "extraction_time": "2025-04-15T01:00:00Z",
                "word_count": 500,
                "reading_time": "3 minutes",
            }
        }
