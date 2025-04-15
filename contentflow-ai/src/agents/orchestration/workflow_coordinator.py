"""Workflow coordinator agent for ContentFlow AI.

This module defines the WorkflowCoordinatorAgent, which is responsible for
orchestrating the workflow between extraction, transformation, and distribution
agents to create seamless content repurposing pipelines.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import uuid

from google.adk.agents import Agent
from google.genai import types

from ..extraction.web_content_agent import WebContentAgent
from ..extraction.video_download_agent import VideoDownloadAgent
from ...models.workflow import WorkflowDefinition, WorkflowExecution, WorkflowStatus


class WorkflowCoordinatorAgent:
    """Agent for coordinating content repurposing workflows.
    
    This agent orchestrates the workflow between extraction, transformation,
    and distribution agents to create seamless content repurposing pipelines.
    It manages the execution of workflow steps, handles errors, and tracks
    the progress of each workflow.
    """
    
    def __init__(self, model: str = "gemini-2.0-pro"):
        """
        Initialize the WorkflowCoordinatorAgent.
        
        Args:
            model: The model to use for the agent (default: gemini-2.0-pro).
        """
        self.agent = Agent(
            name="workflow_coordinator",
            model=model,
            instruction="""
            You are a workflow coordination specialist. Your task is to orchestrate
            content repurposing workflows by coordinating between extraction,
            transformation, and distribution agents. Follow these guidelines:
            
            1. Analyze the workflow definition to understand the steps and dependencies
            2. Execute each step in the correct order, respecting dependencies
            3. Handle errors gracefully and provide meaningful error messages
            4. Track the progress of each workflow and provide status updates
            5. Ensure that the output of each step is properly formatted for the next step
            
            Use the provided agents to execute each step of the workflow and ensure
            that the content flows smoothly through the pipeline.
            """,
            description="Agent that coordinates content repurposing workflows",
            # We don't need to specify tools here as we'll be calling other agents directly
        )
        
        # Initialize the extraction agents
        self.web_content_agent = WebContentAgent(model="gemini-2.0-flash")
        self.video_download_agent = VideoDownloadAgent(model="gemini-2.0-flash")
        
        # We'll initialize transformation and distribution agents as needed
        
    async def execute_workflow(
        self, 
        workflow_definition: WorkflowDefinition,
        input_content_id: str,
        input_content_url: str,
        input_content_type: str,
        parallel: bool = True,
        validate_content: bool = True
    ) -> WorkflowExecution:
        """
        Execute a content repurposing workflow.
        
        Args:
            workflow_definition: The definition of the workflow to execute.
            input_content_id: The ID of the input content.
            input_content_url: The URL of the input content.
            input_content_type: The type of the input content.
            parallel: Whether to execute extraction tasks in parallel (default: True).
            validate_content: Whether to validate content after extraction (default: True).
            
        Returns:
            A WorkflowExecution object containing the execution status and results.
        """
        # Create a new workflow execution
        workflow_execution = WorkflowExecution(
            id=str(uuid.uuid4()),
            workflow_id=workflow_definition.id,
            status=WorkflowStatus.IN_PROGRESS,
            input_content_id=input_content_id,
            started_at=datetime.now(),
        )
        
        try:
            # Log the start of the workflow
            print(f"Starting workflow execution: {workflow_execution.id}")
            print(f"Workflow: {workflow_definition.name}")
            print(f"Input content: {input_content_id} ({input_content_type})")
            print(f"Parallel execution: {parallel}")
            print(f"Content validation: {validate_content}")
            
            # Process the workflow steps
            # First, handle extraction step
            extraction_results = await self._execute_extraction_step(
                workflow_definition=workflow_definition,
                input_content_url=input_content_url,
                input_content_type=input_content_type,
                parallel=parallel,
                validate_content=validate_content
            )
            
            # Store the extracted content IDs
            for content in extraction_results:
                workflow_execution.output_content_ids.append(content["id"])
            
            # TODO: Implement transformation and distribution steps based on the workflow definition
            
            # Mark the workflow as completed
            workflow_execution.status = WorkflowStatus.COMPLETED
            workflow_execution.completed_at = datetime.now()
            workflow_execution.metadata = {
                "extraction_count": len(extraction_results),
                "content_types": [content.get("content_type", "unknown") for content in extraction_results],
                "execution_time": (datetime.now() - workflow_execution.started_at).total_seconds()
            }
            
            # Log the completion of the workflow
            print(f"Workflow execution completed: {workflow_execution.id}")
            print(f"Extracted {len(extraction_results)} content items")
            print(f"Execution time: {workflow_execution.metadata['execution_time']} seconds")
            
        except Exception as e:
            # Handle any errors that occur during workflow execution
            workflow_execution.status = WorkflowStatus.FAILED
            workflow_execution.error = str(e)
            workflow_execution.completed_at = datetime.now()
            
            # Log the error
            print(f"Workflow execution failed: {workflow_execution.id}")
            print(f"Error: {str(e)}")
        
        return workflow_execution
    
    async def _execute_extraction_step(
        self,
        workflow_definition: WorkflowDefinition,
        input_content_url: str,
        input_content_type: str,
        parallel: bool = True,
        validate_content: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute the extraction step of a workflow.
        
        Args:
            workflow_definition: The definition of the workflow to execute.
            input_content_url: The URL of the input content.
            input_content_type: The type of the input content.
            parallel: Whether to execute extraction tasks in parallel.
            validate_content: Whether to validate content after extraction.
            
        Returns:
            A list of dictionaries containing the extracted content with metadata.
        """
        # Determine the extraction tasks to perform
        extraction_tasks = self._determine_extraction_tasks(
            workflow_definition, input_content_url, input_content_type
        )
        
        # Execute the extraction tasks
        if parallel and len(extraction_tasks) > 1:
            # Execute tasks in parallel
            print(f"Executing {len(extraction_tasks)} extraction tasks in parallel")
            results = await asyncio.gather(
                *[self._extract_content(**task) for task in extraction_tasks],
                return_exceptions=True
            )
            
            # Handle any exceptions
            extraction_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Error in extraction task {i}: {str(result)}")
                else:
                    extraction_results.append(result)
        else:
            # Execute tasks sequentially
            print(f"Executing {len(extraction_tasks)} extraction tasks sequentially")
            extraction_results = []
            for i, task in enumerate(extraction_tasks):
                try:
                    result = await self._extract_content(**task)
                    extraction_results.append(result)
                except Exception as e:
                    print(f"Error in extraction task {i}: {str(e)}")
        
        # Validate the extracted content if requested
        if validate_content and extraction_results:
            print(f"Validating {len(extraction_results)} extracted content items")
            validated_results = []
            for content in extraction_results:
                if self._validate_content(content):
                    validated_results.append(content)
                else:
                    print(f"Content validation failed for {content.get('id', 'unknown')}")
            extraction_results = validated_results
        
        # Convert the extracted content to the unified storage format
        unified_results = []
        for content in extraction_results:
            unified_content = self._convert_to_unified_format(content)
            unified_results.append(unified_content)
        
        return unified_results
    
    def _determine_extraction_tasks(
        self,
        workflow_definition: WorkflowDefinition,
        input_content_url: str,
        input_content_type: str
    ) -> List[Dict[str, Any]]:
        """
        Determine the extraction tasks to perform based on the workflow definition.
        
        Args:
            workflow_definition: The definition of the workflow to execute.
            input_content_url: The URL of the input content.
            input_content_type: The type of the input content.
            
        Returns:
            A list of dictionaries containing the extraction tasks to perform.
        """
        # For now, we'll just create a single task based on the input content type
        # In a real implementation, we would analyze the workflow definition to determine
        # what extraction tasks to perform
        tasks = [
            {
                "url": input_content_url,
                "content_type": input_content_type
            }
        ]
        
        # If the content type is video, also extract audio
        if input_content_type == "video":
            tasks.append({
                "url": input_content_url,
                "content_type": "audio"
            })
        
        return tasks
    
    async def _extract_content(self, url: str, content_type: str) -> Dict[str, Any]:
        """
        Extract content from a URL based on the content type.
        
        Args:
            url: The URL to extract content from.
            content_type: The type of content to extract.
            
        Returns:
            A dictionary containing the extracted content with metadata.
        """
        try:
            # Use the appropriate extraction agent based on the content type
            if content_type == "article" or content_type == "web":
                content = await self.web_content_agent.extract_article(url)
                content["content_type"] = "article"
            elif content_type == "video":
                content = await self.video_download_agent.extract_video_metadata(url)
                content["content_type"] = "video"
                # Also extract the transcript if possible
                try:
                    transcript = await self.video_download_agent.extract_video_transcript(url)
                    content["transcript"] = transcript["transcript"]
                except Exception as e:
                    print(f"Error extracting transcript: {str(e)}")
                    content["transcript"] = "Transcript not available"
            elif content_type == "audio":
                # For audio extraction, we need a video path
                # In a real implementation, we would download the video first
                # and then extract the audio
                video_path = f"/tmp/{url.split('/')[-1]}"
                audio_agent = AudioExtractionAgent(model="gemini-2.0-flash")
                content = await audio_agent.extract_audio(
                    video_path=video_path,
                    audio_format="mp3",
                    quality="high"
                )
                content["content_type"] = "audio"
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            # Add a unique ID to the content if it doesn't already have one
            if "id" not in content:
                content["id"] = str(uuid.uuid4())
            
            # Add extraction timestamp
            content["extraction_time"] = datetime.now().isoformat()
            
            return content
            
        except Exception as e:
            # Log the error and re-raise it
            print(f"Error extracting content from {url}: {str(e)}")
            raise
    
    def _validate_content(self, content: Dict[str, Any]) -> bool:
        """
        Validate the extracted content.
        
        Args:
            content: The content to validate.
            
        Returns:
            True if the content is valid, False otherwise.
        """
        # Check that the content has the required fields
        required_fields = ["id", "url", "content_type"]
        for field in required_fields:
            if field not in content:
                print(f"Content is missing required field: {field}")
                return False
        
        # Check content-type specific requirements
        content_type = content.get("content_type")
        if content_type == "article":
            if "title" not in content or "content" not in content:
                print(f"Article content is missing title or content")
                return False
        elif content_type == "video":
            if "title" not in content or "duration" not in content:
                print(f"Video content is missing title or duration")
                return False
        elif content_type == "audio":
            if "output_path" not in content or "format" not in content:
                print(f"Audio content is missing output_path or format")
                return False
        
        return True
    
    def _convert_to_unified_format(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert the extracted content to a unified storage format.
        
        Args:
            content: The content to convert.
            
        Returns:
            The content in the unified storage format.
        """
        # Create a copy of the content to avoid modifying the original
        unified_content = content.copy()
        
        # Add standard metadata fields if they don't exist
        if "metadata" not in unified_content:
            unified_content["metadata"] = {}
        
        # Add extraction timestamp if it doesn't exist
        if "extraction_time" not in unified_content:
            unified_content["extraction_time"] = datetime.now().isoformat()
        
        # Add content type if it doesn't exist
        if "content_type" not in unified_content:
            # Try to determine the content type from the content
            if "title" in unified_content and "content" in unified_content:
                unified_content["content_type"] = "article"
            elif "title" in unified_content and "duration" in unified_content:
                unified_content["content_type"] = "video"
            elif "output_path" in unified_content and "format" in unified_content:
                unified_content["content_type"] = "audio"
            else:
                unified_content["content_type"] = "unknown"
        
        # Add standard fields for all content types
        standard_fields = {
            "id": unified_content.get("id", str(uuid.uuid4())),
            "url": unified_content.get("url", ""),
            "content_type": unified_content.get("content_type", "unknown"),
            "extraction_time": unified_content.get("extraction_time", datetime.now().isoformat()),
            "metadata": unified_content.get("metadata", {}),
        }
        
        # Update the unified content with standard fields
        unified_content.update(standard_fields)
        
        return unified_content
    
    async def get_workflow_status(self, workflow_execution_id: str) -> Dict[str, Any]:
        """
        Get the status of a workflow execution.
        
        Args:
            workflow_execution_id: The ID of the workflow execution.
            
        Returns:
            A dictionary containing the status of the workflow execution.
        """
        # In a real implementation, we would retrieve the workflow execution from a database
        # For now, we'll just return a placeholder
        return {
            "id": workflow_execution_id,
            "status": "completed",
            "started_at": "2025-04-15T01:00:00Z",
            "completed_at": "2025-04-15T01:05:00Z",
            "input_content_id": "sample-content-id",
            "output_content_ids": ["sample-output-id-1", "sample-output-id-2"],
        }
