"""Analytics data models for ContentFlow AI.

This module defines the data models for representing analytics in the ContentFlow AI
platform, including content performance metrics and engagement data.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator


class EngagementType(str, Enum):
    """Enum representing different types of engagement."""
    
    VIEW = "view"
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    CLICK = "click"
    CONVERSION = "conversion"
    SUBSCRIPTION = "subscription"
    DOWNLOAD = "download"
    PLAY = "play"
    OTHER = "other"


class Platform(str, Enum):
    """Enum representing different platforms for content distribution."""
    
    WEBSITE = "website"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    EMAIL = "email"
    PODCAST = "podcast"
    OTHER = "other"


class EngagementMetric(BaseModel):
    """Model for a single engagement metric."""
    
    type: EngagementType = Field(..., description="Type of engagement")
    count: int = Field(..., description="Count of engagements")
    platform: Platform = Field(..., description="Platform where engagement occurred")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the metric was recorded")
    
    @validator("count")
    def validate_count(cls, v):
        """Validate that count is non-negative."""
        if v < 0:
            raise ValueError("Engagement count cannot be negative")
        return v


class ContentPerformance(BaseModel):
    """Model for content performance metrics."""
    
    content_id: str = Field(..., description="ID of the content")
    platform: Platform = Field(..., description="Platform where content was published")
    url: Optional[str] = Field(None, description="URL where content was published")
    published_at: datetime = Field(..., description="When the content was published")
    last_updated: datetime = Field(default_factory=datetime.now, description="When metrics were last updated")
    metrics: Dict[EngagementType, int] = Field(default_factory=dict, description="Engagement metrics")
    reach: Optional[int] = Field(None, description="Number of people who saw the content")
    impressions: Optional[int] = Field(None, description="Number of times the content was displayed")
    engagement_rate: Optional[float] = Field(None, description="Engagement rate as a percentage")
    
    @validator("engagement_rate")
    def validate_engagement_rate(cls, v):
        """Validate that engagement rate is between 0 and 100."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Engagement rate must be between 0 and 100")
        return v


class AudienceSegment(BaseModel):
    """Model for audience segment data."""
    
    name: str = Field(..., description="Name of the audience segment")
    description: Optional[str] = Field(None, description="Description of the audience segment")
    criteria: Dict[str, Any] = Field(..., description="Criteria defining the segment")
    size: Optional[int] = Field(None, description="Size of the segment")
    created_at: datetime = Field(default_factory=datetime.now, description="When the segment was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When the segment was last updated")


class PerformanceByAudience(BaseModel):
    """Model for content performance by audience segment."""
    
    content_id: str = Field(..., description="ID of the content")
    segment_id: str = Field(..., description="ID of the audience segment")
    platform: Platform = Field(..., description="Platform where content was published")
    metrics: Dict[EngagementType, int] = Field(default_factory=dict, description="Engagement metrics")
    engagement_rate: Optional[float] = Field(None, description="Engagement rate as a percentage")
    
    @validator("engagement_rate")
    def validate_engagement_rate(cls, v):
        """Validate that engagement rate is between 0 and 100."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Engagement rate must be between 0 and 100")
        return v


class ContentInsight(BaseModel):
    """Model for insights derived from content performance."""
    
    content_id: str = Field(..., description="ID of the content")
    insight_type: str = Field(..., description="Type of insight")
    description: str = Field(..., description="Description of the insight")
    confidence: float = Field(..., description="Confidence level of the insight (0-1)")
    generated_at: datetime = Field(default_factory=datetime.now, description="When the insight was generated")
    supporting_data: Dict[str, Any] = Field(default_factory=dict, description="Data supporting the insight")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations based on the insight")
    
    @validator("confidence")
    def validate_confidence(cls, v):
        """Validate that confidence is between 0 and 1."""
        if v < 0 or v > 1:
            raise ValueError("Confidence must be between 0 and 1")
        return v


class AnalyticsDashboard(BaseModel):
    """Model for an analytics dashboard configuration."""
    
    id: str = Field(..., description="Unique identifier for the dashboard")
    name: str = Field(..., description="Name of the dashboard")
    description: Optional[str] = Field(None, description="Description of the dashboard")
    owner_id: str = Field(..., description="ID of the dashboard owner")
    created_at: datetime = Field(default_factory=datetime.now, description="When the dashboard was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When the dashboard was last updated")
    widgets: List[Dict[str, Any]] = Field(default_factory=list, description="Widgets in the dashboard")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Filters applied to the dashboard")
    time_range: Dict[str, Any] = Field(default_factory=dict, description="Time range for the dashboard data")
    is_public: bool = Field(default=False, description="Whether the dashboard is public")
    shared_with: List[str] = Field(default_factory=list, description="IDs of users the dashboard is shared with")
