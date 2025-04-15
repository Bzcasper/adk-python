"""Agent orchestration system for ContentFlow AI.

This module provides orchestration capabilities for ContentFlow AI agents,
enabling workflow coordination, parallel processing, and robust error handling.
"""

from typing import Dict, List, Optional, Any, Union, Callable, Awaitable, Set, Type
import asyncio
import uuid
import logging
import time
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from ..communication import (
    MessageType,
    AgentMessage,
    MessageBus,
    AgentCommunicator,
    message_bus,
)

logger = logging.getLogger("contentflow.orchestration")


class WorkflowStatus(str, Enum):
    """Status of a workflow."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    """Status of a task in a workflow."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowTask:
    """A task in a workflow."""
    id: str
    name: str
    agent_id: str
    action: str
    parameters: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class Workflow:
    """A workflow definition and execution state."""
    id: str
    name: str
    description: str
    tasks: Dict[str, WorkflowTask]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    task_order: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    @property
    def is_complete(self) -> bool:
        """Check if all tasks are complete."""
        return all(
            task.status in [TaskStatus.COMPLETED, TaskStatus.SKIPPED]
            for task in self.tasks.values()
        )
    
    @property
    def has_failed(self) -> bool:
        """Check if any task has failed."""
        return any(
            task.status == TaskStatus.FAILED
            for task in self.tasks.values()
        )
        
    @property
    def next_tasks(self) -> List[WorkflowTask]:
        """Get the next tasks that can be executed."""
        result = []
        for task_id in self.task_order:
            task = self.tasks[task_id]
            if task.status == TaskStatus.PENDING:
                # Check if all dependencies are complete
                if all(
                    self.tasks[dep].status == TaskStatus.COMPLETED
                    for dep in task.dependencies
                ):
                    result.append(task)
        return result


class WorkflowCoordinatorAgent:
    """
    Agent for coordinating workflows between agents.
    
    Manages workflow execution, tracks state, and handles errors and retries.
    """
    
    def __init__(self, agent_id: str, agent_name: str = "Workflow Coordinator"):
        """
        Initialize a workflow coordinator agent.
        
        Args:
            agent_id: The ID of the agent.
            agent_name: The name of the agent.
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.communicator = AgentCommunicator(agent_id, agent_name)
        self.workflows: Dict[str, Workflow] = {}
        self.active_tasks: Dict[str, str] = {}  # task_id -> message_id
        self.response_handlers: Dict[str, Callable[[AgentMessage], Awaitable[None]]] = {}
        
    async def start(self):
        """Start the workflow coordinator agent."""
        # Register handlers for different message types
        self.communicator.register_handler(MessageType.RESPONSE, self._handle_response)
        self.communicator.register_handler(MessageType.ERROR, self._handle_error)
        self.communicator.register_handler(MessageType.STATUS, self._handle_status)
        
        # Start the communicator
        await self.communicator.start()
        logger.info(f"Workflow coordinator agent {self.agent_name} ({self.agent_id}) started.")
        
        # Start workflow processing
        asyncio.create_task(self._process_workflows())
        
    async def _process_workflows(self):
        """Process workflows and execute tasks."""
        while True:
            # Process each active workflow
            for workflow_id, workflow in list(self.workflows.items()):
                if workflow.status == WorkflowStatus.RUNNING:
                    # Check if workflow is complete
                    if workflow.is_complete:
                        workflow.status = WorkflowStatus.COMPLETED
                        workflow.completed_at = time.time()
                        logger.info(f"Workflow {workflow.name} ({workflow_id}) completed.")
                        continue
                    
                    # Check if workflow has failed
                    if workflow.has_failed:
                        workflow.status = WorkflowStatus.FAILED
                        workflow.completed_at = time.time()
                        logger.error(f"Workflow {workflow.name} ({workflow_id}) failed.")
                        continue
                    
                    # Find next tasks to execute
                    next_tasks = workflow.next_tasks
                    for task in next_tasks:
                        # Check if task is already active
                        if task.id in self.active_tasks:
                            continue
                        
                        # Execute task
                        asyncio.create_task(self._execute_task(workflow_id, task.id))
            
            # Sleep to avoid high CPU usage
            await asyncio.sleep(0.1)
    
    async def _execute_task(self, workflow_id: str, task_id: str):
        """
        Execute a task in a workflow.
        
        Args:
            workflow_id: The ID of the workflow.
            task_id: The ID of the task to execute.
        """
        workflow = self.workflows[workflow_id]
        task = workflow.tasks[task_id]
        
        # Update task status
        task.status = TaskStatus.RUNNING
        task.start_time = time.time()
        
        # Send request to agent
        try:
            message_id = await self.communicator.send_request(
                recipient=task.agent_id,
                payload={
                    "action": task.action,
                    "parameters": task.parameters,
                    "task_id": task.id,
                    "workflow_id": workflow_id,
                }
            )
            
            # Store message ID for tracking
            self.active_tasks[task.id] = message_id
            
            logger.info(f"Started task {task.name} ({task.id}) in workflow {workflow.name} ({workflow_id}).")
        except Exception as e:
            # Handle task execution error
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.end_time = time.time()
            
            logger.error(f"Error executing task {task.name} ({task.id}): {str(e)}")
    
    async def _handle_response(self, message: AgentMessage):
        """
        Handle a response message from an agent.
        
        Args:
            message: The response message.
        """
        # Find the task this response is for
        task_id = None
        for tid, mid in self.active_tasks.items():
            if mid == message.correlation_id:
                task_id = tid
                break
        
        if task_id is None:
            logger.warning(f"Received response for unknown task: {message.correlation_id}")
            return
        
        # Get workflow and task
        workflow_id = message.payload.get("workflow_id")
        if workflow_id not in self.workflows:
            logger.warning(f"Received response for unknown workflow: {workflow_id}")
            return
        
        workflow = self.workflows[workflow_id]
        task = workflow.tasks[task_id]
        
        # Update task status
        task.status = TaskStatus.COMPLETED
        task.result = message.payload.get("result", {})
        task.end_time = time.time()
        
        # Remove from active tasks
        del self.active_tasks[task_id]
        
        logger.info(f"Task {task.name} ({task.id}) completed in workflow {workflow.name} ({workflow_id}).")
        
        # Call any registered response handler
        if message.correlation_id in self.response_handlers:
            try:
                await self.response_handlers[message.correlation_id](message)
            except Exception as e:
                logger.error(f"Error in response handler: {str(e)}")
            finally:
                del self.response_handlers[message.correlation_id]
    
    async def _handle_error(self, message: AgentMessage):
        """
        Handle an error message from an agent.
        
        Args:
            message: The error message.
        """
        # Find the task this error is for
        task_id = None
        for tid, mid in self.active_tasks.items():
            if mid == message.correlation_id:
                task_id = tid
                break
        
        if task_id is None:
            logger.warning(f"Received error for unknown task: {message.correlation_id}")
            return
        
        # Get workflow and task
        workflow_id = message.payload.get("workflow_id")
        if workflow_id not in self.workflows:
            logger.warning(f"Received error for unknown workflow: {workflow_id}")
            return
        
        workflow = self.workflows[workflow_id]
        task = workflow.tasks[task_id]
        
        # Check if we should retry
        if task.retry_count < task.max_retries:
            # Retry task
            task.retry_count += 1
            task.status = TaskStatus.PENDING
            task.start_time = None
            task.end_time = None
            
            # Remove from active tasks
            del self.active_tasks[task_id]
            
            logger.info(f"Retrying task {task.name} ({task.id}) (attempt {task.retry_count}/{task.max_retries}).")
        else:
            # Mark task as failed
            task.status = TaskStatus.FAILED
            task.error = message.payload.get("error", "Unknown error")
            task.end_time = time.time()
            
            # Remove from active tasks
            del self.active_tasks[task_id]
            
            logger.error(f"Task {task.name} ({task.id}) failed after {task.retry_count} retries: {task.error}")
    
    async def _handle_status(self, message: AgentMessage):
        """
        Handle a status message from an agent.
        
        Args:
            message: The status message.
        """
        # Update task status if applicable
        task_id = message.payload.get("task_id")
        if task_id is None:
            return
        
        workflow_id = message.payload.get("workflow_id")
        if workflow_id not in self.workflows:
            return
        
        workflow = self.workflows[workflow_id]
        if task_id not in workflow.tasks:
            return
        
        # Log status update
        status = message.payload.get("status", {})
        logger.info(f"Status update for task {task_id} in workflow {workflow_id}: {status}")
    
    async def create_workflow(
        self,
        name: str,
        description: str,
        tasks: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a new workflow.
        
        Args:
            name: The name of the workflow.
            description: The description of the workflow.
            tasks: The tasks in the workflow.
            metadata: Optional metadata for the workflow.
            
        Returns:
            The ID of the created workflow.
        """
        workflow_id = str(uuid.uuid4())
        
        # Create workflow tasks
        workflow_tasks = {}
        task_order = []
        
        for task_data in tasks:
            task_id = task_data.get("id", str(uuid.uuid4()))
            task = WorkflowTask(
                id=task_id,
                name=task_data["name"],
                agent_id=task_data["agent_id"],
                action=task_data["action"],
                parameters=task_data.get("parameters", {}),
                dependencies=task_data.get("dependencies", []),
                max_retries=task_data.get("max_retries", 3),
            )
            workflow_tasks[task_id] = task
            task_order.append(task_id)
        
        # Create workflow
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            tasks=workflow_tasks,
            task_order=task_order,
            metadata=metadata or {},
        )
        
        # Store workflow
        self.workflows[workflow_id] = workflow
        
        logger.info(f"Created workflow {name} ({workflow_id}) with {len(workflow_tasks)} tasks.")
        
        return workflow_id
    
    async def start_workflow(self, workflow_id: str) -> bool:
        """
        Start a workflow.
        
        Args:
            workflow_id: The ID of the workflow to start.
            
        Returns:
            True if the workflow was started, False otherwise.
        """
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found.")
            return False
        
        workflow = self.workflows[workflow_id]
        if workflow.status != WorkflowStatus.PENDING:
            logger.error(f"Workflow {workflow_id} is not in PENDING state (current state: {workflow.status}).")
            return False
        
        # Update workflow status
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = time.time()
        
        logger.info(f"Started workflow {workflow.name} ({workflow_id}).")
        
        return True
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """
        Cancel a workflow.
        
        Args:
            workflow_id: The ID of the workflow to cancel.
            
        Returns:
            True if the workflow was cancelled, False otherwise.
        """
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found.")
            return False
        
        workflow = self.workflows[workflow_id]
        if workflow.status not in [WorkflowStatus.PENDING, WorkflowStatus.RUNNING, WorkflowStatus.PAUSED]:
            logger.error(f"Workflow {workflow_id} cannot be cancelled (current state: {workflow.status}).")
            return False
        
        # Update workflow status
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = time.time()
        
        # Cancel active tasks
        for task_id, message_id in list(self.active_tasks.items()):
            task = workflow.tasks.get(task_id)
            if task:
                logger.info(f"Cancelling task {task.name} ({task_id}).")
        
        logger.info(f"Cancelled workflow {workflow.name} ({workflow_id}).")
        
        return True
    
    async def pause_workflow(self, workflow_id: str) -> bool:
        """
        Pause a workflow.
        
        Args:
            workflow_id: The ID of the workflow to pause.
            
        Returns:
            True if the workflow was paused, False otherwise.
        """
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found.")
            return False
        
        workflow = self.workflows[workflow_id]
        if workflow.status != WorkflowStatus.RUNNING:
            logger.error(f"Workflow {workflow_id} is not in RUNNING state (current state: {workflow.status}).")
            return False
        
        # Update workflow status
        workflow.status = WorkflowStatus.PAUSED
        
        logger.info(f"Paused workflow {workflow.name} ({workflow_id}).")
        
        return True
    
    async def resume_workflow(self, workflow_id: str) -> bool:
        """
        Resume a paused workflow.
        
        Args:
            workflow_id: The ID of the workflow to resume.
            
        Returns:
            True if the workflow was resumed, False otherwise.
        """
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found.")
            return False
        
        workflow = self.workflows[workflow_id]
        if workflow.status != WorkflowStatus.PAUSED:
            logger.error(f"Workflow {workflow_id} is not in PAUSED state (current state: {workflow.status}).")
            return False
        
        # Update workflow status
        workflow.status = WorkflowStatus.RUNNING
        
        logger.info(f"Resumed workflow {workflow.name} ({workflow_id}).")
        
        return True
    
    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get workflow details.
        
        Args:
            workflow_id: The ID of the workflow to get.
            
        Returns:
            The workflow details, or None if the workflow was not found.
        """
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found.")
            return None
        
        workflow = self.workflows[workflow_id]
        
        # Convert workflow to dict
        result = {
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
            "status": workflow.status,
            "created_at": workflow.created_at,
            "started_at": workflow.started_at,
            "completed_at": workflow.completed_at,
            "metadata": workflow.metadata,
            "error": workflow.error,
            "tasks": {},
        }
        
        # Add tasks
        for task_id, task in workflow.tasks.items():
            result["tasks"][task_id] = {
                "id": task.id,
                "name": task.name,
                "agent_id": task.agent_id,
                "action": task.action,
                "parameters": task.parameters,
                "status": task.status,
                "dependencies": task.dependencies,
                "result": task.result,
                "error": task.error,
                "start_time": task.start_time,
                "end_time": task.end_time,
                "retry_count": task.retry_count,
                "max_retries": task.max_retries,
            }
        
        return result
    
    async def get_workflows(self, status: Optional[WorkflowStatus] = None) -> List[Dict[str, Any]]:
        """
        Get all workflows.
        
        Args:
            status: Optional status to filter by.
            
        Returns:
            A list of workflow summaries.
        """
        result = []
        
        for workflow_id, workflow in self.workflows.items():
            if status is not None and workflow.status != status:
                continue
            
            # Add workflow summary
            result.append({
                "id": workflow.id,
                "name": workflow.name,
                "description": workflow.description,
                "status": workflow.status,
                "created_at": workflow.created_at,
                "started_at": workflow.started_at,
                "completed_at": workflow.completed_at,
                "task_count": len(workflow.tasks),
                "completed_tasks": sum(1 for task in workflow.tasks.values() if task.status == TaskStatus.COMPLETED),
                "error": workflow.error,
            })
        
        return result
