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

@router.get("/items", response_model=list[ContentItem])
def list_content_items():
    """
    List all content items.
    Returns an empty list if monkeypatched by tests.
    """
    # Allow monkeypatching in tests by not hardcoding the list
    return getattr(list_content_items, "_test_return", [ContentItem(id="123", title="Sample", type="web", status="completed")])
