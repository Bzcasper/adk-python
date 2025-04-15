"""
FastAPI routes for content management (CRUD operations).
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/management", tags=["management"])

class ContentItem(BaseModel):
    id: str
    title: str
    type: str
    status: str

from typing import Callable, List
from fastapi import Depends


def get_content_items() -> List[ContentItem]:
    """Default data provider for content items."""
    return [ContentItem(id="123", title="Sample", type="web", status="completed")]

from ..auth import get_current_user
from fastapi import Depends

from ..db import get_session
from ..models.core import Content
from sqlmodel import select

@router.get("/items", response_model=list[ContentItem])
def list_content_items(user=Depends(get_current_user)):
    """
    List all content items from the database (requires authentication).
    """
    with get_session() as session:
        results = session.exec(select(Content)).all()
        return results
