"""
Minimal Modal deployment for ContentFlow AI API.

This is a simplified version that should work with any Modal CLI version.

Usage:
    modal deploy src/api/minimal_deploy.py
"""
from modal import App, Image, asgi_app
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import os

# Create a simple app
app = App("contentflow-minimal")

# Configure a more complete image with database and auth support
image = (
    Image.debian_slim()
    .pip_install(
        "fastapi==0.103.1", 
        "uvicorn==0.23.2",
        "sqlmodel==0.0.8",
        "python-jose[cryptography]==3.4.0",
        "python-multipart==0.0.6",
        "psycopg2-binary==2.9.7"
    )
)

# Auth models
class User(BaseModel):
    username: str
    role: str = "user"

class TokenData(BaseModel):
    sub: str
    role: str = "user"
    exp: int = 0

# JWT settings
SECRET_KEY = "dev-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"

# Auth functions
def create_jwt_token(data: dict):
    from jose import jwt
    import time
    
    to_encode = data.copy()
    to_encode.update({"exp": int(time.time()) + 3600})  # 1 hour expiration
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(authorization: str = None):
    from jose import jwt, JWTError
    
    if not authorization or not authorization.startswith("Bearer "):
        return User(username="anonymous")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role", "user")
        
        if not username:
            return User(username="anonymous")
            
        return User(username=username, role=role)
    except JWTError:
        return User(username="anonymous")

# Define the web endpoint
@app.function(
    image=image,
    timeout=300,
)
@asgi_app()
def fastapi_app():
    """
    Deploy a ContentFlow AI FastAPI application with database integration.
    """
    from fastapi import Header, HTTPException, status
    from fastapi.middleware.cors import CORSMiddleware
    from sqlmodel import SQLModel, create_engine, Session, select, Field
    from typing import List, Optional
    from datetime import datetime
    from uuid import uuid4, UUID
    import os
    
    # Create FastAPI app
    api = FastAPI(title="ContentFlow AI API")
    
    # Add CORS middleware
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Database setup
    DATABASE_URL = os.environ.get("CFLOW_DB_URL", "sqlite:///./contentflow.db")
    engine = create_engine(DATABASE_URL, echo=True)
    
    # Define models
    class Content(SQLModel, table=True):
        id: UUID = Field(default_factory=uuid4, primary_key=True)
        title: str
        type: str
        source_url: Optional[str] = None
        status: str = "pending"
        created_at: datetime = Field(default_factory=datetime.utcnow)
        updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Sample data function
    def get_sample_data():
        return [
            Content(id=uuid4(), title="Sample Content", type="web", source_url="https://example.com", status="completed"),
            Content(id=uuid4(), title="Example Article", type="web", source_url="https://example.org", status="pending")
        ]
    
    # Initialize database with sample data
    with Session(engine) as session:
        result = session.exec(select(Content)).first()
        if not result:
            for item in get_sample_data():
                session.add(item)
            session.commit()
    
    # Routes
    @api.get("/")
    def read_root():
        return {"message": "Welcome to ContentFlow AI API"}
    
    @api.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    @api.get("/api/content")
    def list_content(authorization: Optional[str] = Header(None)):
        user = get_current_user(authorization)
        
        with Session(engine) as session:
            results = session.exec(select(Content)).all()
            return results
    
    @api.post("/api/token")
    def create_token(username: str = "test-user", role: str = "user"):
        token = create_jwt_token({"sub": username, "role": role})
        return {"access_token": token, "token_type": "bearer"}
    
    return api
