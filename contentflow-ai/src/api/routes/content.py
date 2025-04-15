"""
FastAPI routes for content extraction.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/content", tags=["content"])

class ContentExtractRequest(BaseModel):
    url: str
    type: str

class ContentExtractResponse(BaseModel):
    id: str
    status: str
    message: str

from ..auth import get_current_user
from fastapi import Depends

from ..db import get_session
from ..models.core import Content, ContentType
from sqlmodel import Session
import uuid
from datetime import datetime

@router.post("/extract", response_model=ContentExtractResponse)
def extract_content(request: ContentExtractRequest, user=Depends(get_current_user)):
    """
    Extract content from a given URL (requires authentication).
    Stores a Content record in the DB.
    """
    with get_session() as session:
        content = Content(
            id=uuid.uuid4(),
            source_url=request.url,
            type=ContentType(request.type),
            title=None,
            description=None,
            metadata=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(content)
        session.commit()
        session.refresh(content)
        return ContentExtractResponse(id=str(content.id), status="pending", message=f"Extraction started by {user.username}.")
