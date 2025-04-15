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

@router.post("/extract", response_model=ContentExtractResponse)
def extract_content(request: ContentExtractRequest):
    """
    Extract content from a given URL.
    """
    # Placeholder for extraction logic
    return ContentExtractResponse(id="123", status="pending", message="Extraction started.")
