"""Tests for the TextTransformationAgent.

This module contains tests for the TextTransformationAgent in ContentFlow AI.
"""

import pytest
import asyncio
import os
from typing import Dict, Any
from unittest.mock import patch, MagicMock, AsyncMock

from src.agents.transformation.text_transformation_agent import TextTransformationAgent


@pytest.fixture
def text_transformation_agent():
    """Create a TextTransformationAgent for testing."""
    return TextTransformationAgent(model="gemini-2.0-flash", vllm_model="mistral-7b")


@pytest.mark.asyncio
class TestTextTransformationAgent:
    """Tests for the TextTransformationAgent class."""

    async def test_summarize_text_with_vllm(self, text_transformation_agent):
        """Test summarizing text with vLLM."""
        # Test parameters
        text = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
        nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
        eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt 
        in culpa qui officia deserunt mollit anim id est laborum.
        """
        max_length = 50
        style = "informative"
        format = "paragraph"
        
        # Mock the vLLM service
        with patch('src.models.serving.vllm_service.generate_text.remote', new_callable=AsyncMock) as mock_generate_text:
            # Set up the mock return value
            mock_generate_text.return_value = {
                "status": "success",
                "model_name": "mistral-7b",
                "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
                "prompt": "test prompt",
                "generated_text": "This is a summarized version of the text that captures the main points while being concise.",
                "load_time": 0.5,
                "generation_time": 1.2,
                "total_time": 1.7,
                "timestamp": "2025-04-15T02:00:00.000000",
                "parameters": {
                    "max_tokens": 100,
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "top_k": 50,
                    "repetition_penalty": 1.1,
                    "use_torch_compile": True,
                },
            }
            
            # Call the summarize_text method
            result = await text_transformation_agent.summarize_text(
                text=text,
                max_length=max_length,
                style=style,
                format=format
            )
            
            # Verify the result
            assert result is not None
            assert "id" in result
            assert "original_text" in result
            assert "summary" in result
            assert "transformation_type" in result
            assert "parameters" in result
            assert "model" in result
            assert "metadata" in result
            assert "timestamp" in result
            
            # Verify specific values
            assert result["transformation_type"] == "summarization"
            assert result["parameters"]["max_length"] == max_length
            assert result["parameters"]["style"] == style
            assert result["parameters"]["format"] == format
            assert result["model"]["name"] == "mistral-7b"
            assert result["model"]["provider"] == "vllm"
            
            # Verify the summary
            assert result["summary"] == "This is a summarized version of the text that captures the main points while being concise."
            
            # Verify that generate_text was called with the correct parameters
            mock_generate_text.assert_called_once()
            args, kwargs = mock_generate_text.call_args
            assert kwargs["model_name"] == "mistral-7b"
            assert kwargs["temperature"] == 0.3
            assert kwargs["use_torch_compile"] is True

    async def test_summarize_text_with_fallback(self, text_transformation_agent):
        """Test summarizing text with fallback to ADK agent."""
        # Test parameters
        text = "This is a test text that needs to be summarized."
        max_length = 50
        style = "informative"
        format = "paragraph"
        
        # Mock the vLLM service to raise an exception
        with patch('src.models.serving.vllm_service.generate_text.remote', new_callable=AsyncMock) as mock_generate_text:
            mock_generate_text.side_effect = Exception("vLLM service unavailable")
            
            # Mock the ADK agent
            with patch.object(
                text_transformation_agent.agent, 
                'generate_content_async',
                new_callable=AsyncMock
            ) as mock_generate_content:
                # Set up the mock return value
                mock_response = MagicMock()
                mock_response.text = "This is a summary from the ADK agent."
                mock_generate_content.return_value = mock_response
                
                # Call the summarize_text method
                result = await text_transformation_agent.summarize_text(
                    text=text,
                    max_length=max_length,
                    style=style,
                    format=format
                )
                
                # Verify the result
                assert result is not None
                assert "id" in result
                assert "original_text" in result
                assert "summary" in result
                assert "transformation_type" in result
                assert "parameters" in result
                assert "model" in result
                assert "metadata" in result
                assert "timestamp" in result
                
                # Verify specific values
                assert result["transformation_type"] == "summarization"
                assert result["parameters"]["max_length"] == max_length
                assert result["parameters"]["style"] == style
                assert result["parameters"]["format"] == format
                assert result["model"]["name"] == "gemini-2.0-pro"
                assert result["model"]["provider"] == "google"
                
                # Verify the summary
                assert result["summary"] == "This is a summary from the ADK agent."
                
                # Verify that generate_content_async was called
                mock_generate_content.assert_called_once()

    async def test_change_style(self, text_transformation_agent):
        """Test changing text style."""
        # Test parameters
        text = "This is a casual text that needs to be transformed to a formal style."
        target_style = "formal"
        preserve_meaning = True
        format = "paragraph"
        
        # Mock the vLLM service
        with patch('src.models.serving.vllm_service.generate_text.remote', new_callable=AsyncMock) as mock_generate_text:
            # Set up the mock return value
            mock_generate_text.return_value = {
                "status": "success",
                "model_name": "mistral-7b",
                "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
                "prompt": "test prompt",
                "generated_text": "This is a formal version of the text that maintains the original meaning.",
                "load_time": 0.5,
                "generation_time": 1.2,
                "total_time": 1.7,
                "timestamp": "2025-04-15T02:00:00.000000",
                "parameters": {
                    "max_tokens": 100,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 50,
                    "repetition_penalty": 1.1,
                    "use_torch_compile": True,
                },
            }
            
            # Call the change_style method
            result = await text_transformation_agent.change_style(
                text=text,
                target_style=target_style,
                preserve_meaning=preserve_meaning,
                format=format
            )
            
            # Verify the result
            assert result is not None
            assert "id" in result
            assert "original_text" in result
            assert "transformed_text" in result
            assert "transformation_type" in result
            assert "parameters" in result
            assert "model" in result
            assert "metadata" in result
            assert "timestamp" in result
            
            # Verify specific values
            assert result["transformation_type"] == "style_transfer"
            assert result["parameters"]["target_style"] == target_style
            assert result["parameters"]["preserve_meaning"] == preserve_meaning
            assert result["parameters"]["format"] == format
            assert result["model"]["name"] == "mistral-7b"
            assert result["model"]["provider"] == "vllm"
            
            # Verify the transformed text
            assert result["transformed_text"] == "This is a formal version of the text that maintains the original meaning."

    async def test_convert_format(self, text_transformation_agent):
        """Test converting text format."""
        # Test parameters
        text = "This is a plain text that needs to be converted to markdown."
        target_format = "markdown"
        preserve_content = True
        add_metadata = False
        
        # Mock the vLLM service
        with patch('src.models.serving.vllm_service.generate_text.remote', new_callable=AsyncMock) as mock_generate_text:
            # Set up the mock return value
            mock_generate_text.return_value = {
                "status": "success",
                "model_name": "mistral-7b",
                "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
                "prompt": "test prompt",
                "generated_text": "# This is a markdown version\n\nOf the plain text that was provided.",
                "load_time": 0.5,
                "generation_time": 1.2,
                "total_time": 1.7,
                "timestamp": "2025-04-15T02:00:00.000000",
                "parameters": {
                    "max_tokens": 100,
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "top_k": 50,
                    "repetition_penalty": 1.1,
                    "use_torch_compile": True,
                },
            }
            
            # Call the convert_format method
            result = await text_transformation_agent.convert_format(
                text=text,
                target_format=target_format,
                preserve_content=preserve_content,
                add_metadata=add_metadata
            )
            
            # Verify the result
            assert result is not None
            assert "id" in result
            assert "original_text" in result
            assert "converted_text" in result
            assert "transformation_type" in result
            assert "parameters" in result
            assert "model" in result
            assert "metadata" in result
            assert "timestamp" in result
            
            # Verify specific values
            assert result["transformation_type"] == "format_conversion"
            assert result["parameters"]["target_format"] == target_format
            assert result["parameters"]["preserve_content"] == preserve_content
            assert result["parameters"]["add_metadata"] == add_metadata
            assert result["model"]["name"] == "mistral-7b"
            assert result["model"]["provider"] == "vllm"
            
            # Verify the converted text
            assert result["converted_text"] == "# This is a markdown version\n\nOf the plain text that was provided."
