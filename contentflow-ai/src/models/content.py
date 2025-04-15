"""Content data models for ContentFlow AI.

This module defines the data models for representing content in the ContentFlow AI
platform, including different content types and their metadata.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, HttpUrl


class ContentType(str, Enum):
    """Enum representing different types of content."""
    
    ARTICLE = "article"
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    SOCIAL_POST = "social_post"
    EMAIL = "email"
    PRESENTATION = "presentation"
    DOCUMENT = "document"
    OTHER = "other"


class ContentSource(str, Enum):
    """Enum representing different sources of content."""
    
    WEB = "web"
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    PODCAST = "podcast"
    UPLOAD = "upload"
    GENERATED = "generated"
    OTHER = "other"


class ContentMetadata(BaseModel):
    """Base metadata for all content types."""
    
    source: ContentSource = Field(..., description="Source of the content")
    source_url: Optional[HttpUrl] = Field(None, description="URL of the original content")
    extracted_at: datetime = Field(default_factory=datetime.now, description="When the content was extracted")
    language: str = Field("en", description="Language of the content (ISO 639-1 code)")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the content")
    word_count: Optional[int] = Field(None, description="Number of words in the content")
    reading_time: Optional[int] = Field(None, description="Estimated reading time in seconds")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata fields")


class ArticleContent(BaseModel):
    """Model for article content."""
    
    title: str = Field(..., description="Title of the article")
    subtitle: Optional[str] = Field(None, description="Subtitle of the article")
    author: Optional[str] = Field(None, description="Author of the article")
    published_date: Optional[datetime] = Field(None, description="When the article was published")
    content: str = Field(..., description="Main content of the article")
    summary: Optional[str] = Field(None, description="Summary of the article")
    sections: List[Dict[str, str]] = Field(default_factory=list, description="Sections of the article")
    images: List[HttpUrl] = Field(default_factory=list, description="URLs of images in the article")


class VideoContent(BaseModel):
    """Model for video content."""
    
    title: str = Field(..., description="Title of the video")
    creator: Optional[str] = Field(None, description="Creator of the video")
    published_date: Optional[datetime] = Field(None, description="When the video was published")
    duration: int = Field(..., description="Duration of the video in seconds")
    description: Optional[str] = Field(None, description="Description of the video")
    transcript: Optional[str] = Field(None, description="Transcript of the video")
    file_path: Optional[str] = Field(None, description="Local path to the video file")
    thumbnail_url: Optional[HttpUrl] = Field(None, description="URL of the video thumbnail")
    resolution: Optional[str] = Field(None, description="Resolution of the video")
    format: Optional[str] = Field(None, description="Format of the video")


class AudioContent(BaseModel):
    """Model for audio content."""
    
    title: str = Field(..., description="Title of the audio")
    creator: Optional[str] = Field(None, description="Creator of the audio")
    published_date: Optional[datetime] = Field(None, description="When the audio was published")
    duration: int = Field(..., description="Duration of the audio in seconds")
    description: Optional[str] = Field(None, description="Description of the audio")
    transcript: Optional[str] = Field(None, description="Transcript of the audio")
    file_path: Optional[str] = Field(None, description="Local path to the audio file")
    format: Optional[str] = Field(None, description="Format of the audio")


class SocialPostContent(BaseModel):
    """Model for social media post content."""
    
    platform: str = Field(..., description="Social media platform")
    text: str = Field(..., description="Text content of the post")
    author: Optional[str] = Field(None, description="Author of the post")
    published_date: Optional[datetime] = Field(None, description="When the post was published")
    hashtags: List[str] = Field(default_factory=list, description="Hashtags in the post")
    mentions: List[str] = Field(default_factory=list, description="Mentions in the post")
    media_urls: List[HttpUrl] = Field(default_factory=list, description="URLs of media in the post")
    engagement: Optional[Dict[str, int]] = Field(None, description="Engagement metrics")


class Content(BaseModel):
    """Main content model that can represent any type of content."""
    
    id: str = Field(..., description="Unique identifier for the content")
    type: ContentType = Field(..., description="Type of content")
    metadata: ContentMetadata = Field(..., description="Metadata about the content")
    content: Union[ArticleContent, VideoContent, AudioContent, SocialPostContent, Dict[str, Any]] = Field(
        ..., description="The actual content data"
    )
    
    class Config:
        """Pydantic configuration."""
        
        arbitrary_types_allowed = True
