"""Tests for workflow orchestration.

This module contains tests for the workflow orchestration system in ContentFlow AI.
"""

import pytest
import asyncio
from typing import Dict, Any, List
import uuid

from src.agents.orchestration.workflow import (
    WorkflowStatus,
    TaskStatus,
    WorkflowTask,
    Workflow,
    WorkflowCoordinatorAgent,
)

from src.agents.orchestration.workflow_definition import (
    TaskType,
    ExecutionMode,
    WorkflowDefinition,
    TaskDefinition,
    WorkflowMetadata,
    create_content_extraction_workflow,
)

from src.agents.communication import (
    MessageType,
    AgentMessage,
    AgentCommunicator,
)


@pytest.fixture
def web_content_agent():
    """Web content agent mock."""
    agent = AgentCommunicator(agent_id="web-content-agent", agent_name="Web Content Agent")
    return agent


@pytest.fixture
def video_agent():
    """Video agent mock."""
    agent = AgentCommunicator(agent_id="video-download-agent", agent_name="Video Download Agent")
    return agent


@pytest.fixture
def audio_agent():
    """Audio agent mock."""
    agent = AgentCommunicator(agent_id="audio-extraction-agent", agent_name="Audio Extraction Agent")
    return agent


@pytest.fixture
def workflow_coordinator():
    """Workflow coordinator agent."""
    agent = WorkflowCoordinatorAgent(agent_id="workflow-coordinator")
    return agent


@pytest.mark.asyncio
class TestWorkflowDefinition:
    """Tests for workflow definition."""
    
    async def test_create_content_extraction_workflow(self):
        """Test creating a content extraction workflow."""
        url = "https://example.com"
        workflow = create_content_extraction_workflow(
            url=url,
            creator="test-user",
            include_video=True,
            include_audio=True,
        )
        
        # Check workflow properties
        assert workflow.name == f"Content Extraction: {url}"
        assert "Extract content from" in workflow.description
        assert workflow.metadata.created_by == "test-user"
        assert "extraction" in workflow.metadata.tags
        assert workflow.execution_mode == ExecutionMode.SEQUENTIAL
        
        # Check tasks
        assert len(workflow.tasks) == 3  # Web, Video, and Audio extraction
        
        # Check web task
        web_task = workflow.tasks[0]
        assert web_task.name == "Web Content Extraction"
        assert web_task.type == TaskType.EXTRACTION
        assert web_task.agent_id == "web-content-agent"
        assert web_task.action == "extract_content"
        assert web_task.parameters["url"] == url
        
        # Check video task
        video_task = workflow.tasks[1]
        assert video_task.name == "Video Extraction"
        assert video_task.type == TaskType.EXTRACTION
        assert video_task.agent_id == "video-download-agent"
        assert video_task.dependencies == [web_task.id]
        
        # Check audio task
        audio_task = workflow.tasks[2]
        assert audio_task.name == "Audio Extraction"
        assert audio_task.type == TaskType.EXTRACTION
        assert audio_task.agent_id == "audio-extraction-agent"
        assert audio_task.dependencies == [video_task.id]
    
    async def test_create_content_extraction_workflow_no_video(self):
        """Test creating a content extraction workflow without video."""
        url = "https://example.com"
        workflow = create_content_extraction_workflow(
            url=url,
            creator="test-user",
            include_video=False,
            include_audio=False,
        )
        
        # Check tasks - should only have web extraction
        assert len(workflow.tasks) == 1
        assert workflow.tasks[0].name == "Web Content Extraction"


@pytest.mark.asyncio
class TestWorkflowCoordinator:
    """Tests for workflow coordinator."""
    
    async def test_create_workflow(self, workflow_coordinator):
        """Test creating a workflow."""
        workflow_id = await workflow_coordinator.create_workflow(
            name="Test Workflow",
            description="A test workflow",
            tasks=[
                {
                    "name": "Task 1",
                    "agent_id": "agent1",
                    "action": "test_action",
                    "parameters": {"param1": "value1"},
                }
            ],
            metadata={"test_key": "test_value"},
        )
        
        assert workflow_id is not None
        assert workflow_id in workflow_coordinator.workflows
        
        workflow = workflow_coordinator.workflows[workflow_id]
        assert workflow.name == "Test Workflow"
        assert workflow.description == "A test workflow"
        assert workflow.status == WorkflowStatus.PENDING
        assert len(workflow.tasks) == 1
        assert workflow.metadata == {"test_key": "test_value"}
        
        task = list(workflow.tasks.values())[0]
        assert task.name == "Task 1"
        assert task.agent_id == "agent1"
        assert task.action == "test_action"
        assert task.parameters == {"param1": "value1"}
        assert task.status == TaskStatus.PENDING
    
    async def test_workflow_lifecycle(self, workflow_coordinator):
        """Test workflow lifecycle (start, pause, resume, cancel)."""
        # Create workflow
        workflow_id = await workflow_coordinator.create_workflow(
            name="Lifecycle Test",
            description="Testing workflow lifecycle",
            tasks=[
                {
                    "name": "Long Task",
                    "agent_id": "agent1",
                    "action": "long_action",
                    "parameters": {},
                }
            ],
        )
        
        # Start workflow
        result = await workflow_coordinator.start_workflow(workflow_id)
        assert result is True
        assert workflow_coordinator.workflows[workflow_id].status == WorkflowStatus.RUNNING
        
        # Pause workflow
        result = await workflow_coordinator.pause_workflow(workflow_id)
        assert result is True
        assert workflow_coordinator.workflows[workflow_id].status == WorkflowStatus.PAUSED
        
        # Resume workflow
        result = await workflow_coordinator.resume_workflow(workflow_id)
        assert result is True
        assert workflow_coordinator.workflows[workflow_id].status == WorkflowStatus.RUNNING
        
        # Cancel workflow
        result = await workflow_coordinator.cancel_workflow(workflow_id)
        assert result is True
        assert workflow_coordinator.workflows[workflow_id].status == WorkflowStatus.CANCELLED
    
    async def test_get_workflow(self, workflow_coordinator):
        """Test getting workflow details."""
        # Create workflow
        workflow_id = await workflow_coordinator.create_workflow(
            name="Details Test",
            description="Testing workflow details",
            tasks=[
                {
                    "name": "Task A",
                    "agent_id": "agent1",
                    "action": "action_a",
                    "parameters": {"param": "value"},
                },
                {
                    "name": "Task B",
                    "agent_id": "agent2",
                    "action": "action_b",
                    "parameters": {},
                    "dependencies": ["task_a_id"],
                },
            ],
        )
        
        # Get workflow details
        workflow_details = await workflow_coordinator.get_workflow(workflow_id)
        
        assert workflow_details is not None
        assert workflow_details["name"] == "Details Test"
        assert workflow_details["description"] == "Testing workflow details"
        assert workflow_details["status"] == WorkflowStatus.PENDING
        assert len(workflow_details["tasks"]) == 2
        
        # Get all workflows
        all_workflows = await workflow_coordinator.get_workflows()
        assert len(all_workflows) >= 1
        assert any(w["id"] == workflow_id for w in all_workflows)
        
        # Get workflows by status
        pending_workflows = await workflow_coordinator.get_workflows(status=WorkflowStatus.PENDING)
        assert any(w["id"] == workflow_id for w in pending_workflows)


@pytest.mark.asyncio
class TestWorkflowExecution:
    """Integration tests for workflow execution."""
    
    async def test_simple_workflow_execution(self, workflow_coordinator, web_content_agent):
        """Test execution of a simple workflow."""
        # Setup response handler for web content agent
        received_requests = []
        
        async def handle_request(message):
            received_requests.append(message)
            # Send response back
            await web_content_agent.send_response(
                recipient=message.sender,
                payload={
                    "workflow_id": message.payload["workflow_id"],
                    "result": {
                        "title": "Example Page",
                        "content": "Example content",
                        "metadata": {"author": "Test Author"},
                    }
                },
                correlation_id=message.id,
            )
        
        # Register handler and start agent
        web_content_agent.register_handler(MessageType.REQUEST, handle_request)
        await web_content_agent.start()
        await workflow_coordinator.start()
        
        # Create a simple workflow
        workflow_id = await workflow_coordinator.create_workflow(
            name="Simple Test",
            description="Simple workflow execution test",
            tasks=[
                {
                    "name": "Extract Web Content",
                    "agent_id": "web-content-agent",
                    "action": "extract_content",
                    "parameters": {"url": "https://example.com"},
                }
            ],
        )
        
        # Start workflow
        await workflow_coordinator.start_workflow(workflow_id)
        
        # Wait for execution
        await asyncio.sleep(0.5)
        
        # Get workflow details
        workflow_details = await workflow_coordinator.get_workflow(workflow_id)
        
        # Verify workflow completed
        assert workflow_details["status"] == WorkflowStatus.COMPLETED
        
        # Verify task completed
        task_id = list(workflow_details["tasks"].keys())[0]
        task = workflow_details["tasks"][task_id]
        assert task["status"] == TaskStatus.COMPLETED
        assert task["result"]["title"] == "Example Page"
        assert task["result"]["content"] == "Example content"
        
        # Verify agent received request
        assert len(received_requests) == 1
        assert received_requests[0].payload["action"] == "extract_content"
        assert received_requests[0].payload["parameters"]["url"] == "https://example.com"
