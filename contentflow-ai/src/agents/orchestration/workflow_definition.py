"""Workflow definition schemas for ContentFlow AI.

This module provides schema definitions for creating workflows in ContentFlow AI.
It enables structured workflow creation with validations and best practices.
"""

from typing import Dict, List, Optional, Any, Union, Set
from enum import Enum
from pydantic import BaseModel, Field, validator
import uuid
from datetime import datetime


class TaskType(str, Enum):
    """Types of tasks in ContentFlow AI workflows."""
    EXTRACTION = "extraction"
    TRANSFORMATION = "transformation"
    DISTRIBUTION = "distribution"
    ORCHESTRATION = "orchestration"
    CUSTOM = "custom"


class ExecutionMode(str, Enum):
    """Execution modes for workflow tasks."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"


class WorkflowMetadata(BaseModel):
    """Metadata for a workflow."""
    created_by: str
    tags: List[str] = Field(default_factory=list)
    priority: int = 1
    description: Optional[str] = None
    custom_properties: Dict[str, Any] = Field(default_factory=dict)


class TaskParameter(BaseModel):
    """Parameter definition for a workflow task."""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None
    validation: Optional[str] = None
    

class TaskDefinition(BaseModel):
    """Definition of a task in a workflow."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    type: TaskType
    agent_id: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    parameter_schema: List[TaskParameter] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    timeout_seconds: int = 300
    retry_policy: Dict[str, Any] = Field(
        default_factory=lambda: {
            "max_retries": 3,
            "retry_interval": 5,
            "backoff_factor": 2,
        }
    )
    
    @validator('dependencies')
    def validate_dependencies(cls, v, values):
        """Validate that dependencies don't include the task itself."""
        if 'id' in values and values['id'] in v:
            raise ValueError(f"Task '{values['id']}' cannot depend on itself")
        return v


class ConditionDefinition(BaseModel):
    """Definition of a condition for conditional execution."""
    source_task: str
    condition_type: str  # "equals", "contains", "greater_than", etc.
    field: str  # Field in task result to check
    value: Any  # Value to compare against
    description: Optional[str] = None


class WorkflowBranch(BaseModel):
    """Definition of a workflow branch for conditional execution."""
    name: str
    description: Optional[str] = None
    condition: ConditionDefinition
    tasks: List[TaskDefinition]


class WorkflowDefinition(BaseModel):
    """Definition of a workflow in ContentFlow AI."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    metadata: WorkflowMetadata
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    tasks: List[TaskDefinition] = Field(default_factory=list)
    branches: List[WorkflowBranch] = Field(default_factory=list)
    version: str = "1.0"
    
    @validator('tasks')
    def validate_tasks(cls, v):
        """Validate that task IDs are unique."""
        task_ids = set()
        for task in v:
            if task.id in task_ids:
                raise ValueError(f"Duplicate task ID: {task.id}")
            task_ids.add(task.id)
        return v
    
    @validator('branches')
    def validate_branches(cls, v, values):
        """Validate branch conditions reference existing tasks."""
        if 'tasks' in values:
            task_ids = {task.id for task in values['tasks']}
            for branch in v:
                if branch.condition.source_task not in task_ids:
                    raise ValueError(
                        f"Branch condition references non-existing task: {branch.condition.source_task}"
                    )
                
                # Check branch task dependencies
                for task in branch.tasks:
                    for dep in task.dependencies:
                        if dep not in task_ids and not any(
                            dep == t.id for t in branch.tasks
                        ):
                            raise ValueError(
                                f"Task '{task.id}' depends on non-existing task: {dep}"
                            )
        return v


def create_content_extraction_workflow(
    url: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    creator: str = "system",
    include_video: bool = True,
    include_audio: bool = True,
) -> WorkflowDefinition:
    """
    Create a standard content extraction workflow.
    
    Args:
        url: URL to extract content from
        name: Optional workflow name (defaults to 'Content Extraction: {url}')
        description: Optional workflow description
        creator: Creator of the workflow
        include_video: Whether to include video extraction
        include_audio: Whether to include audio extraction
        
    Returns:
        A complete workflow definition ready for execution
    """
    if not name:
        name = f"Content Extraction: {url}"
        
    if not description:
        description = f"Extract content from {url} with metadata and media processing"
    
    # Create web extraction task
    web_task = TaskDefinition(
        name="Web Content Extraction",
        description=f"Extract content and metadata from {url}",
        type=TaskType.EXTRACTION,
        agent_id="web-content-agent",
        action="extract_content",
        parameters={"url": url, "include_metadata": True},
    )
    
    tasks = [web_task]
    
    # Add video extraction if requested
    if include_video:
        video_task = TaskDefinition(
            name="Video Extraction",
            description="Extract videos from the website",
            type=TaskType.EXTRACTION,
            agent_id="video-download-agent",
            action="extract_videos",
            parameters={"url": url},
            dependencies=[web_task.id],
        )
        tasks.append(video_task)
        
        # Add audio extraction if requested
        if include_audio:
            audio_task = TaskDefinition(
                name="Audio Extraction",
                description="Extract audio from videos",
                type=TaskType.EXTRACTION,
                agent_id="audio-extraction-agent",
                action="extract_audio",
                parameters={"process_all": True},
                dependencies=[video_task.id],
            )
            tasks.append(audio_task)
    
    # Create workflow metadata
    metadata = WorkflowMetadata(
        created_by=creator,
        tags=["extraction", "content", "web"],
        priority=2,
        description=f"Automatic content extraction workflow for {url}",
    )
    
    # Create workflow definition
    workflow = WorkflowDefinition(
        name=name,
        description=description,
        metadata=metadata,
        execution_mode=ExecutionMode.SEQUENTIAL,
        tasks=tasks,
    )
    
    return workflow


def create_content_transformation_workflow(
    content_id: str,
    output_formats: List[str],
    name: Optional[str] = None,
    description: Optional[str] = None,
    creator: str = "system",
) -> WorkflowDefinition:
    """
    Create a standard content transformation workflow.
    
    Args:
        content_id: ID of the content to transform
        output_formats: List of output formats (e.g., "article", "summary", "social_post")
        name: Optional workflow name (defaults to 'Content Transformation: {content_id}')
        description: Optional workflow description
        creator: Creator of the workflow
        
    Returns:
        A complete workflow definition ready for execution
    """
    if not name:
        name = f"Content Transformation: {content_id}"
        
    if not description:
        format_str = ", ".join(output_formats)
        description = f"Transform content {content_id} into formats: {format_str}"
    
    # Create the content loading task
    load_task = TaskDefinition(
        name="Load Content",
        description=f"Load content {content_id} for transformation",
        type=TaskType.TRANSFORMATION,
        agent_id="content-loader-agent",
        action="load_content",
        parameters={"content_id": content_id},
    )
    
    tasks = [load_task]
    
    # Add transformation tasks for each output format
    for output_format in output_formats:
        transform_task = TaskDefinition(
            name=f"Transform to {output_format.capitalize()}",
            description=f"Transform content to {output_format} format",
            type=TaskType.TRANSFORMATION,
            agent_id="content-transformer-agent",
            action="transform_content",
            parameters={
                "content_id": content_id,
                "output_format": output_format,
            },
            dependencies=[load_task.id],
        )
        tasks.append(transform_task)
    
    # Create workflow metadata
    metadata = WorkflowMetadata(
        created_by=creator,
        tags=["transformation", "content"],
        priority=2,
        description=f"Content transformation workflow for {content_id}",
    )
    
    # Create workflow definition
    workflow = WorkflowDefinition(
        name=name,
        description=description,
        metadata=metadata,
        execution_mode=ExecutionMode.PARALLEL,
        tasks=tasks,
    )
    
    return workflow
