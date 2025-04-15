"""
API schema models for ContentFlow AI.

This module defines Pydantic models for API request/response validation.
These are separate from the SQLModel database models to allow for API-specific
validation and documentation.
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from uuid import UUID


class ContentExtractRequest(BaseModel):
    """
    Request model for content extraction.
    
    Args:
        url: URL to extract content from
        type: Type of content (web, video, audio, etc.)
        options: Optional extraction parameters
    """
    url: str
    type: str
    options: Optional[Dict[str, Any]] = None


class ContentExtractResponse(BaseModel):
    """
    Response model for content extraction.
    
    Args:
        id: Unique identifier for the extraction job
        status: Status of the extraction (pending, processing, completed, failed)
        message: Optional status message
        error: Optional error message
    """
    id: str
    status: str
    message: Optional[str] = None
    error: Optional[str] = None


class ProcessingRequest(BaseModel):
    """
    Request model for content processing.
    
    Args:
        content_id: ID of the content to process
        operation: Processing operation to perform
        params: Optional processing parameters
    """
    content_id: str
    operation: str
    params: Optional[Dict[str, Any]] = {}


class ProcessingResponse(BaseModel):
    """
    Response model for content processing.
    
    Args:
        result: Processing result data
        status: Status of the processing (success, failed)
        error: Optional error message
    """
    result: Dict[str, Any]
    status: str
    error: Optional[str] = None


class ContentItem(BaseModel):
    """
    Model for a content item in the API.
    
    Args:
        id: Unique identifier
        title: Content title
        type: Content type
        status: Processing status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    title: Optional[str] = None
    type: str
    status: str
    source_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
