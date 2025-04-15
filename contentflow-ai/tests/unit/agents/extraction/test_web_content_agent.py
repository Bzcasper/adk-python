"""Unit tests for the WebContentAgent.

This module contains unit tests for the WebContentAgent, which is responsible
for extracting content from websites using crawl4ai.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from google.genai import types

# Use relative imports for testing
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from src.agents.extraction.web_content_agent import WebContentAgent


@pytest.fixture
def mock_agent():
    """Create a mock agent for testing."""
    with patch('google.adk.agents.Agent') as mock_agent_class:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock()
        mock_agent_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def web_content_agent(mock_agent):
    """Create a WebContentAgent instance with a mocked underlying agent."""
    return WebContentAgent(model="test-model")


def test_extract_web_content_calls_agent(web_content_agent, mock_agent):
    """Test that extract_web_content calls the underlying agent with the correct parameters."""
    # Arrange
    url = "https://example.com"
    selectors = {"title": "h1", "content": "article"}
    
    # Mock the agent's response
    mock_response = MagicMock()
    mock_agent.generate_content_async.return_value = mock_response
    
    # Act
    result = asyncio.run(web_content_agent.extract_web_content(url, selectors))
    
    # Assert
    mock_agent.generate_content_async.assert_called_once()
    # Check that the URL and selectors were included in the request
    call_args = mock_agent.generate_content_async.call_args[0][0]
    assert isinstance(call_args, types.Content)
    assert url in call_args.parts[0].text
    assert str(selectors) in call_args.parts[0].text
    
    # Check the structure of the result
    assert "url" in result
    assert "title" in result
    assert "content" in result
    assert "metadata" in result
    assert result["url"] == url


def test_extract_article_calls_agent(web_content_agent, mock_agent):
    """Test that extract_article calls the underlying agent with the correct parameters."""
    # Arrange
    url = "https://example.com/article"
    
    # Mock the agent's response
    mock_response = MagicMock()
    mock_agent.generate_content_async.return_value = mock_response
    
    # Act
    result = asyncio.run(web_content_agent.extract_article(url))
    
    # Assert
    mock_agent.generate_content_async.assert_called_once()
    # Check that the URL was included in the request
    call_args = mock_agent.generate_content_async.call_args[0][0]
    assert isinstance(call_args, types.Content)
    assert url in call_args.parts[0].text
    
    # Check the structure of the result
    assert "url" in result
    assert "title" in result
    assert "author" in result
    assert "published_date" in result
    assert "content" in result
    assert "images" in result
    assert "metadata" in result
    assert result["url"] == url


def test_extract_web_content_with_default_selectors(web_content_agent, mock_agent):
    """Test that extract_web_content works with default selectors."""
    # Arrange
    url = "https://example.com"
    
    # Mock the agent's response
    mock_response = MagicMock()
    mock_agent.generate_content_async.return_value = mock_response
    
    # Act
    result = asyncio.run(web_content_agent.extract_web_content(url))
    
    # Assert
    mock_agent.generate_content_async.assert_called_once()
    # Check that the URL was included in the request
    call_args = mock_agent.generate_content_async.call_args[0][0]
    assert isinstance(call_args, types.Content)
    assert url in call_args.parts[0].text
    assert "Use default selectors" in call_args.parts[0].text
    
    # Check the structure of the result
    assert "url" in result
    assert "title" in result
    assert "content" in result
    assert "metadata" in result
    assert result["url"] == url
