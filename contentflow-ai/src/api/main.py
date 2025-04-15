"""
FastAPI application entry point for ContentFlow AI API.
"""
from fastapi import FastAPI
from .routes import content, processing, management

app = FastAPI(title="ContentFlow AI API")

app.include_router(content.router)
app.include_router(processing.router)
app.include_router(management.router)

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"status": "ok", "message": "ContentFlow AI API is running."}
