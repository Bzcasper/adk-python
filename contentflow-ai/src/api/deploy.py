"""
Modal deployment for ContentFlow AI API.

This module configures the FastAPI application for serverless deployment
on Modal Labs infrastructure.

Usage:
    # First activate the environment
    python scripts/env_manager.py activate [dev|test|prod]
    
    # Then deploy
    modal deploy src/api/deploy.py
"""
import os
import sys
from pathlib import Path
from modal import Image, App, asgi_app

# Add project root to path to ensure imports work
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Create Modal app
app = App("contentflow-api")

# Configure deployment image
api_image = (
    Image.debian_slim()
    .pip_install(
        "fastapi==0.103.1",
        "sqlmodel==0.0.8",
        "python-jose[cryptography]==3.3.0",
        "python-multipart==0.0.6",
        "alembic==1.12.0",
        "psycopg2-binary==2.9.7",
        "pydantic==2.4.2",
        "uvicorn==0.23.2",
    )
    .apt_install("ffmpeg")
)

# Add local directory to the image
api_image = api_image.add_local_dir(str(project_root), remote_path="/app")

# Define the web endpoint
@app.function(
    image=api_image,
    timeout=600,
    # No mounts - using add_local_dir instead
)
@asgi_app()
def fastapi_app():
    """
    Deploy the ContentFlow AI FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    # Get environment settings
    env_name = os.environ.get("CFLOW_ENVIRONMENT", "dev")
    db_url = os.environ.get("CFLOW_DB_URL", "sqlite:///./dev.db")
    jwt_secret = os.environ.get("CFLOW_JWT_SECRET", "dev-secret-key")
    
    # Set environment variables for the app
    os.environ["CFLOW_DB_URL"] = db_url
    os.environ["CFLOW_JWT_SECRET"] = jwt_secret
    
    # Import and configure the FastAPI app
    from src.api.main import app
    
    # Initialize database if needed (for SQLite)
    if db_url.startswith("sqlite"):
        from src.api.db import init_db
        init_db()
    
    return app
