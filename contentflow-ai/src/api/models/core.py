"""
Core database models for ContentFlow AI.

Defines Content, Extraction, Workflow, and WorkflowTask tables using SQLModel.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship, Column, JSON


class ContentType(str, Enum):
    web = "web"
    video = "video"
    other = "other"


class ExtractionStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class WorkflowStatus(str, Enum):
    created = "created"
    running = "running"
    completed = "completed"
    failed = "failed"


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"


class Content(SQLModel, table=True):
    """
    Content record (web, video, etc).

    Args:
        id (UUID): Primary key.
        source_url (str): Original content source URL.
        type (ContentType): Content type.
        title (str): Title.
        description (str): Description.
        metadata (dict): Extra metadata.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    source_url: Optional[str] = Field(default=None)
    type: ContentType
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    extractions: list["Extraction"] = Relationship(back_populates="content")


class Extraction(SQLModel, table=True):
    """
    Extraction record by an agent for content.

    Args:
        id (UUID): Primary key.
        content_id (UUID): FK to Content.
        agent (str): Agent name.
        status (ExtractionStatus): Status.
        result (dict): Extraction result.
        error_message (str): Error details.
        started_at (datetime): Start time.
        completed_at (datetime): End time.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    content_id: UUID = Field(foreign_key="content.id")
    agent: str
    status: ExtractionStatus
    result: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    content: Optional[Content] = Relationship(back_populates="extractions")


class Workflow(SQLModel, table=True):
    """
    Workflow definition and execution state.

    Args:
        id (UUID): Primary key.
        name (str): Workflow name.
        definition (dict): Workflow definition.
        status (WorkflowStatus): Status.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    definition: dict = Field(sa_column=Column(JSON))
    status: WorkflowStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    tasks: list["WorkflowTask"] = Relationship(back_populates="workflow")


class WorkflowTask(SQLModel, table=True):
    """
    Task within a workflow.

    Args:
        id (UUID): Primary key.
        workflow_id (UUID): FK to Workflow.
        task_name (str): Task name.
        status (TaskStatus): Task status.
        result (dict): Task result.
        error_message (str): Error details.
        started_at (datetime): Start time.
        completed_at (datetime): End time.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    workflow_id: UUID = Field(foreign_key="workflow.id")
    task_name: str
    status: TaskStatus
    result: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    workflow: Optional[Workflow] = Relationship(back_populates="tasks")
