"""
Unit tests for ContentFlow AI core database models (Content, Extraction, Workflow, WorkflowTask).
"""
import pytest
from sqlmodel import Session, SQLModel, create_engine
from uuid import UUID
from datetime import datetime

from contentflow_ai.src.api.models.core import (
    Content, Extraction, Workflow, WorkflowTask,
    ContentType, ExtractionStatus, WorkflowStatus, TaskStatus
)

def setup_memory_db():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


def test_content_creation():
    engine = setup_memory_db()
    with Session(engine) as session:
        content = Content(
            source_url="https://example.com",
            type=ContentType.web,
            title="Test Title",
            description="Test Desc",
            metadata={"lang": "en"}
        )
        session.add(content)
        session.commit()
        assert content.id is not None
        assert content.type == ContentType.web
        assert content.metadata["lang"] == "en"


def test_extraction_creation():
    engine = setup_memory_db()
    with Session(engine) as session:
        content = Content(source_url=None, type=ContentType.video)
        session.add(content)
        session.commit()
        extraction = Extraction(
            content_id=content.id,
            agent="WebContentAgent",
            status=ExtractionStatus.pending
        )
        session.add(extraction)
        session.commit()
        assert extraction.id is not None
        assert extraction.agent == "WebContentAgent"
        assert extraction.status == ExtractionStatus.pending


def test_workflow_and_task():
    engine = setup_memory_db()
    with Session(engine) as session:
        workflow = Workflow(
            name="Main Workflow",
            definition={"steps": []},
            status=WorkflowStatus.created
        )
        session.add(workflow)
        session.commit()
        task = WorkflowTask(
            workflow_id=workflow.id,
            task_name="Extract Content",
            status=TaskStatus.pending
        )
        session.add(task)
        session.commit()
        assert task.id is not None
        assert task.status == TaskStatus.pending
        assert task.workflow_id == workflow.id


def test_content_type_enum_edge_case():
    # Should raise ValueError for invalid enum
    with pytest.raises(ValueError):
        Content(type="invalid_type")


def test_missing_required_field():
    with pytest.raises(TypeError):
        Content()  # type is required


def test_extraction_status_failure_case():
    engine = setup_memory_db()
    with Session(engine) as session:
        content = Content(source_url=None, type=ContentType.web)
        session.add(content)
        session.commit()
        extraction = Extraction(
            content_id=content.id,
            agent="VideoDownloadAgent",
            status=ExtractionStatus.failed,
            error_message="Download error"
        )
        session.add(extraction)
        session.commit()
        assert extraction.status == ExtractionStatus.failed
        assert extraction.error_message == "Download error"
