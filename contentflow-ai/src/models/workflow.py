"""Workflow data models for ContentFlow AI.

This module defines the data models for representing workflows in the ContentFlow AI
platform, including workflow definitions, steps, and execution status.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator

from .content import ContentType


class WorkflowStepType(str, Enum):
    """Enum representing different types of workflow steps."""
    
    EXTRACTION = "extraction"
    TRANSFORMATION = "transformation"
    DISTRIBUTION = "distribution"
    ANALYSIS = "analysis"
    CUSTOM = "custom"


class WorkflowStepStatus(str, Enum):
    """Enum representing the status of a workflow step."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStatus(str, Enum):
    """Enum representing the status of a workflow."""
    
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStepDefinition(BaseModel):
    """Definition of a workflow step."""
    
    id: str = Field(..., description="Unique identifier for the step")
    name: str = Field(..., description="Name of the step")
    description: Optional[str] = Field(None, description="Description of the step")
    type: WorkflowStepType = Field(..., description="Type of the step")
    agent: str = Field(..., description="Agent responsible for executing the step")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration for the step")
    depends_on: List[str] = Field(default_factory=list, description="IDs of steps this step depends on")
    
    @validator("depends_on")
    def validate_dependencies(cls, v, values):
        """Validate that a step doesn't depend on itself."""
        if "id" in values and values["id"] in v:
            raise ValueError("A step cannot depend on itself")
        return v


class WorkflowDefinition(BaseModel):
    """Definition of a workflow."""
    
    id: str = Field(..., description="Unique identifier for the workflow")
    name: str = Field(..., description="Name of the workflow")
    description: Optional[str] = Field(None, description="Description of the workflow")
    created_at: datetime = Field(default_factory=datetime.now, description="When the workflow was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When the workflow was last updated")
    input_type: ContentType = Field(..., description="Type of content the workflow accepts as input")
    output_types: List[ContentType] = Field(..., description="Types of content the workflow produces as output")
    steps: List[WorkflowStepDefinition] = Field(..., description="Steps in the workflow")
    
    @validator("steps")
    def validate_steps(cls, v):
        """Validate that the workflow has at least one step and that dependencies exist."""
        if not v:
            raise ValueError("Workflow must have at least one step")
        
        step_ids = {step.id for step in v}
        for step in v:
            for dep_id in step.depends_on:
                if dep_id not in step_ids:
                    raise ValueError(f"Step {step.id} depends on non-existent step {dep_id}")
        
        return v


class WorkflowStepExecution(BaseModel):
    """Execution of a workflow step."""
    
    step_id: str = Field(..., description="ID of the step definition")
    status: WorkflowStepStatus = Field(default=WorkflowStepStatus.PENDING, description="Status of the step")
    started_at: Optional[datetime] = Field(None, description="When the step was started")
    completed_at: Optional[datetime] = Field(None, description="When the step was completed")
    error: Optional[str] = Field(None, description="Error message if the step failed")
    output: Optional[Dict[str, Any]] = Field(None, description="Output of the step")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Metrics about the step execution")


class WorkflowExecution(BaseModel):
    """Execution of a workflow."""
    
    id: str = Field(..., description="Unique identifier for the workflow execution")
    workflow_id: str = Field(..., description="ID of the workflow definition")
    status: WorkflowStatus = Field(default=WorkflowStatus.DRAFT, description="Status of the workflow")
    created_at: datetime = Field(default_factory=datetime.now, description="When the workflow execution was created")
    scheduled_for: Optional[datetime] = Field(None, description="When the workflow is scheduled to run")
    started_at: Optional[datetime] = Field(None, description="When the workflow was started")
    completed_at: Optional[datetime] = Field(None, description="When the workflow was completed")
    input_content_id: str = Field(..., description="ID of the input content")
    output_content_ids: List[str] = Field(default_factory=list, description="IDs of the output content")
    steps: Dict[str, WorkflowStepExecution] = Field(default_factory=dict, description="Execution status of each step")
    error: Optional[str] = Field(None, description="Error message if the workflow failed")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Metrics about the workflow execution")


class WorkflowTemplate(BaseModel):
    """Template for creating workflows."""
    
    id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Name of the template")
    description: Optional[str] = Field(None, description="Description of the template")
    created_at: datetime = Field(default_factory=datetime.now, description="When the template was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When the template was last updated")
    input_type: ContentType = Field(..., description="Type of content the template accepts as input")
    output_types: List[ContentType] = Field(..., description="Types of content the template produces as output")
    workflow_definition: WorkflowDefinition = Field(..., description="Definition of the workflow")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the template")
    category: Optional[str] = Field(None, description="Category of the template")
    popularity: int = Field(default=0, description="Popularity score of the template")
