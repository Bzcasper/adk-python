"""Text transformation agent for ContentFlow AI.

This module defines the TextTransformationAgent, which is responsible for transforming
text content using high-performance language models. It leverages the vLLM service
for efficient inference and supports various text transformation tasks such as
summarization, style transfer, and format conversion.
"""

from typing import Dict, List, Optional, Any
import os
import json
from datetime import datetime
import uuid
import asyncio

from google.adk.agents import Agent
from google.genai import types

from ...models.serving.vllm_service import generate_text


class TextTransformationAgent:
    """Agent for transforming text content.
    
    This agent uses high-performance language models to transform text content
    for various purposes such as summarization, style transfer, and format conversion.
    It leverages the vLLM service for efficient inference.
    """
    
    def __init__(self, model: str = "gemini-2.0-pro", vllm_model: str = "mistral-7b"):
        """
        Initialize the TextTransformationAgent.
        
        Args:
            model: The ADK model to use for the agent (default: gemini-2.0-pro).
            vllm_model: The vLLM model to use for text transformation (default: mistral-7b).
        """
        self.agent = Agent(
            name="text_transformer",
            model=model,
            instruction="""
            You are a text transformation specialist. Your task is to transform text content
            for various purposes. Follow these guidelines:
            
            1. Analyze the input text to understand its structure and content
            2. Apply the requested transformation (summarization, style transfer, etc.)
            3. Ensure the output maintains the key information from the input
            4. Format the output according to the requested format
            5. Provide metadata about the transformation process
            
            Use the provided tools to transform text content efficiently.
            """,
            description="Agent that transforms text content using high-performance language models",
            # We'll use the vLLM service directly rather than through tools
        )
        
        self.vllm_model = vllm_model
    
    async def summarize_text(
        self, 
        text: str, 
        max_length: int = 500,
        style: str = "informative",
        format: str = "paragraph"
    ) -> Dict[str, Any]:
        """
        Summarize text content.
        
        Args:
            text: The text to summarize.
            max_length: The maximum length of the summary in words (default: 500).
            style: The style of the summary (default: informative).
            format: The format of the summary (default: paragraph).
            
        Returns:
            A dictionary containing the summarized text and metadata.
        """
        # Create a prompt for the vLLM model
        prompt = f"""
        # Text Summarization Task

        ## Input Text:
        {text}

        ## Summarization Instructions:
        - Create a summary of the above text
        - Maximum length: {max_length} words
        - Style: {style}
        - Format: {format}
        - Preserve the key information and main points
        - Maintain the original tone where appropriate
        
        ## Summary:
        """
        
        # Use the vLLM service to generate the summary
        try:
            result = await generate_text.remote(
                prompt=prompt,
                model_name=self.vllm_model,
                max_tokens=max_length * 2,  # Approximate token count
                temperature=0.3,  # Lower temperature for more focused output
                top_p=0.9,
                repetition_penalty=1.1,
                use_torch_compile=True,
            )
            
            # Extract the summary from the generated text
            summary = result["generated_text"].strip()
            
            # Return the summary and metadata
            return {
                "id": str(uuid.uuid4()),
                "original_text": text[:1000] + "..." if len(text) > 1000 else text,  # Truncate for readability
                "summary": summary,
                "transformation_type": "summarization",
                "parameters": {
                    "max_length": max_length,
                    "style": style,
                    "format": format,
                },
                "model": {
                    "name": self.vllm_model,
                    "provider": "vllm",
                },
                "metadata": {
                    "original_length": len(text),
                    "summary_length": len(summary),
                    "compression_ratio": len(summary) / len(text) if len(text) > 0 else 0,
                    "generation_time": result["generation_time"],
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            # If vLLM fails, fall back to the ADK agent
            print(f"vLLM service failed: {str(e)}. Falling back to ADK agent.")
            
            response = await self.agent.generate_content_async(
                types.Content(
                    parts=[
                        types.Part.from_text(
                            f"Summarize the following text:\n\n{text}\n\n"
                            f"Maximum length: {max_length} words\n"
                            f"Style: {style}\n"
                            f"Format: {format}"
                        )
                    ]
                )
            )
            
            # Extract the summary from the response
            summary = response.text
            
            # Return the summary and metadata
            return {
                "id": str(uuid.uuid4()),
                "original_text": text[:1000] + "..." if len(text) > 1000 else text,  # Truncate for readability
                "summary": summary,
                "transformation_type": "summarization",
                "parameters": {
                    "max_length": max_length,
                    "style": style,
                    "format": format,
                },
                "model": {
                    "name": "gemini-2.0-pro",
                    "provider": "google",
                },
                "metadata": {
                    "original_length": len(text),
                    "summary_length": len(summary),
                    "compression_ratio": len(summary) / len(text) if len(text) > 0 else 0,
                    "fallback": True,
                },
                "timestamp": datetime.now().isoformat(),
            }
    
    async def change_style(
        self, 
        text: str, 
        target_style: str,
        preserve_meaning: bool = True,
        format: str = "paragraph"
    ) -> Dict[str, Any]:
        """
        Change the style of text content.
        
        Args:
            text: The text to transform.
            target_style: The target style (e.g., formal, casual, technical).
            preserve_meaning: Whether to preserve the original meaning (default: True).
            format: The format of the output (default: paragraph).
            
        Returns:
            A dictionary containing the transformed text and metadata.
        """
        # Create a prompt for the vLLM model
        prompt = f"""
        # Style Transfer Task

        ## Input Text:
        {text}

        ## Style Transfer Instructions:
        - Transform the above text to a {target_style} style
        - {"Preserve the original meaning and key information" if preserve_meaning else "Focus on style over exact meaning"}
        - Format: {format}
        - Maintain the same level of detail and information
        
        ## Transformed Text:
        """
        
        # Use the vLLM service to generate the transformed text
        try:
            result = await generate_text.remote(
                prompt=prompt,
                model_name=self.vllm_model,
                max_tokens=len(text.split()) * 2,  # Approximate token count
                temperature=0.7,  # Higher temperature for more creative output
                top_p=0.9,
                repetition_penalty=1.1,
                use_torch_compile=True,
            )
            
            # Extract the transformed text from the generated text
            transformed_text = result["generated_text"].strip()
            
            # Return the transformed text and metadata
            return {
                "id": str(uuid.uuid4()),
                "original_text": text[:1000] + "..." if len(text) > 1000 else text,  # Truncate for readability
                "transformed_text": transformed_text,
                "transformation_type": "style_transfer",
                "parameters": {
                    "target_style": target_style,
                    "preserve_meaning": preserve_meaning,
                    "format": format,
                },
                "model": {
                    "name": self.vllm_model,
                    "provider": "vllm",
                },
                "metadata": {
                    "original_length": len(text),
                    "transformed_length": len(transformed_text),
                    "length_ratio": len(transformed_text) / len(text) if len(text) > 0 else 0,
                    "generation_time": result["generation_time"],
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            # If vLLM fails, fall back to the ADK agent
            print(f"vLLM service failed: {str(e)}. Falling back to ADK agent.")
            
            response = await self.agent.generate_content_async(
                types.Content(
                    parts=[
                        types.Part.from_text(
                            f"Transform the following text to a {target_style} style:\n\n{text}\n\n"
                            f"Preserve meaning: {preserve_meaning}\n"
                            f"Format: {format}"
                        )
                    ]
                )
            )
            
            # Extract the transformed text from the response
            transformed_text = response.text
            
            # Return the transformed text and metadata
            return {
                "id": str(uuid.uuid4()),
                "original_text": text[:1000] + "..." if len(text) > 1000 else text,  # Truncate for readability
                "transformed_text": transformed_text,
                "transformation_type": "style_transfer",
                "parameters": {
                    "target_style": target_style,
                    "preserve_meaning": preserve_meaning,
                    "format": format,
                },
                "model": {
                    "name": "gemini-2.0-pro",
                    "provider": "google",
                },
                "metadata": {
                    "original_length": len(text),
                    "transformed_length": len(transformed_text),
                    "length_ratio": len(transformed_text) / len(text) if len(text) > 0 else 0,
                    "fallback": True,
                },
                "timestamp": datetime.now().isoformat(),
            }
    
    async def convert_format(
        self, 
        text: str, 
        target_format: str,
        preserve_content: bool = True,
        add_metadata: bool = False
    ) -> Dict[str, Any]:
        """
        Convert text to a different format.
        
        Args:
            text: The text to convert.
            target_format: The target format (e.g., markdown, html, json).
            preserve_content: Whether to preserve all content (default: True).
            add_metadata: Whether to add metadata to the output (default: False).
            
        Returns:
            A dictionary containing the converted text and metadata.
        """
        # Create a prompt for the vLLM model
        prompt = f"""
        # Format Conversion Task

        ## Input Text:
        {text}

        ## Format Conversion Instructions:
        - Convert the above text to {target_format} format
        - {"Preserve all content and information" if preserve_content else "Focus on key information only"}
        - {"Include metadata in the output" if add_metadata else "Do not include metadata"}
        - Ensure the output is valid {target_format}
        - Maintain the structure and hierarchy of the content
        
        ## Converted Text:
        """
        
        # Use the vLLM service to generate the converted text
        try:
            result = await generate_text.remote(
                prompt=prompt,
                model_name=self.vllm_model,
                max_tokens=len(text.split()) * 2,  # Approximate token count
                temperature=0.2,  # Lower temperature for more precise output
                top_p=0.9,
                repetition_penalty=1.1,
                use_torch_compile=True,
            )
            
            # Extract the converted text from the generated text
            converted_text = result["generated_text"].strip()
            
            # Return the converted text and metadata
            return {
                "id": str(uuid.uuid4()),
                "original_text": text[:1000] + "..." if len(text) > 1000 else text,  # Truncate for readability
                "converted_text": converted_text,
                "transformation_type": "format_conversion",
                "parameters": {
                    "target_format": target_format,
                    "preserve_content": preserve_content,
                    "add_metadata": add_metadata,
                },
                "model": {
                    "name": self.vllm_model,
                    "provider": "vllm",
                },
                "metadata": {
                    "original_length": len(text),
                    "converted_length": len(converted_text),
                    "length_ratio": len(converted_text) / len(text) if len(text) > 0 else 0,
                    "generation_time": result["generation_time"],
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            # If vLLM fails, fall back to the ADK agent
            print(f"vLLM service failed: {str(e)}. Falling back to ADK agent.")
            
            response = await self.agent.generate_content_async(
                types.Content(
                    parts=[
                        types.Part.from_text(
                            f"Convert the following text to {target_format} format:\n\n{text}\n\n"
                            f"Preserve content: {preserve_content}\n"
                            f"Add metadata: {add_metadata}"
                        )
                    ]
                )
            )
            
            # Extract the converted text from the response
            converted_text = response.text
            
            # Return the converted text and metadata
            return {
                "id": str(uuid.uuid4()),
                "original_text": text[:1000] + "..." if len(text) > 1000 else text,  # Truncate for readability
                "converted_text": converted_text,
                "transformation_type": "format_conversion",
                "parameters": {
                    "target_format": target_format,
                    "preserve_content": preserve_content,
                    "add_metadata": add_metadata,
                },
                "model": {
                    "name": "gemini-2.0-pro",
                    "provider": "google",
                },
                "metadata": {
                    "original_length": len(text),
                    "converted_length": len(converted_text),
                    "length_ratio": len(converted_text) / len(text) if len(text) > 0 else 0,
                    "fallback": True,
                },
                "timestamp": datetime.now().isoformat(),
            }
