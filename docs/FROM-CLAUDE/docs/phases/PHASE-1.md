ContentFlow AI: Detailed Implementation Plan - Phase 1
Days 1-15: Project Setup and Foundation
Day 1: Project Initialization

Create Project Repository

Set up a GitHub repository with the following structure:
contentflow-ai/
├── api/               # Backend API code
├── client/            # Frontend application
├── infrastructure/    # Deployment configurations
├── notebooks/         # Research and testing
├── scripts/           # Utility scripts
├── docs/              # Documentation
└── README.md          # Project overview

Initialize Git with appropriate .gitignore file for Python projects
Add README with project vision and basic setup instructions


Set Up Development Environment

Create a virtual environment:
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install initial dependencies:
bashpip install modal-client fastapi crawl4ai yt-dlp transformers torch
pip install pytest black isort flake8  # Development tools
pip freeze > requirements.txt



Create Modal Labs Account Setup

Sign up for a Modal Labs account if you don't have one
Install the Modal CLI tool:
bashpip install modal

Initialize Modal token:
bashmodal token new

Create your first Modal app configuration file:
python# content_flow_app.py
import modal

# Define the image with base dependencies
image = modal.Image.debian_slim().pip_install(
    "fastapi>=0.95.0",
    "pydantic>=2.0.0",
    "crawl4ai>=0.5.0",
    "yt-dlp>=2025.3.31",
    "transformers>=4.34.0",
    "torch>=2.0.0"
)

# Create the app
app = modal.App("contentflow-ai")

@app.function(image=image)
@modal.web_endpoint()
def hello():
    return {"message": "ContentFlow AI is initialized!"}

if __name__ == "__main__":
    app.serve()

Test the deployment:
bashmodal serve content_flow_app.py




Day 2-3: Core Extraction Module Design

Design Content Extraction API

Create module structure:
api/
├── extractors/
│   ├── __init__.py
│   ├── web_extractor.py      # crawl4ai integration
│   ├── media_extractor.py    # yt-dlp integration
│   └── social_extractor.py   # social media scraping
└── models/
    ├── __init__.py
    └── content.py            # data models for content



Implement Basic Web Extractor

Create web extraction function using crawl4ai:
python# api/extractors/web_extractor.py
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import MarkdownExtractionStrategy

async def extract_web_content(url, include_images=False, max_depth=1):
    """Extract content from a web page."""
    try:
        browser_config = BrowserConfig(
            headless=True,
            ignore_https_errors=True,
            user_agent_type="desktop_chrome_latest"
        )
        
        crawler_config = CrawlerRunConfig(
            extraction_strategy=MarkdownExtractionStrategy(
                include_images=include_images
            ),
            follow_links=max_depth > 1,
            max_links=50 if max_depth > 1 else 0,
            max_crawl_depth=max_depth
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=crawler_config)
            
            return {
                "title": result.metadata.title,
                "description": result.metadata.description,
                "content": result.markdown.original_markdown,
                "text": result.markdown.to_text(),
                "links": result.links,
                "images": result.images if include_images else []
            }
    except Exception as e:
        return {"error": str(e)}

# Function to be exposed via Modal
def extract_web_content_sync(url, include_images=False, max_depth=1):
    """Synchronous wrapper for web content extraction."""
    return asyncio.run(extract_web_content(url, include_images, max_depth))



Implement Basic Media Extractor

Create media extraction function using yt-dlp:
python# api/extractors/media_extractor.py
import os
import tempfile
import subprocess
from typing import Dict, Any, Optional, List

def extract_video_info(url: str) -> Dict[str, Any]:
    """Extract video metadata without downloading."""
    try:
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-playlist",
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}

def extract_video_content(
    url: str,
    output_format: str = "mp4",
    extract_audio: bool = False,
    extract_captions: bool = False,
    temp_dir: Optional[str] = None
) -> Dict[str, Any]:
    """Download video content and return file paths."""
    with tempfile.TemporaryDirectory() as temp:
        work_dir = temp_dir or temp
        output_path = os.path.join(work_dir, "output")
        
        try:
            # Build yt-dlp command
            cmd = ["yt-dlp", "-o", f"{output_path}.%(ext)s"]
            
            if extract_audio:
                cmd.extend(["-x", "--audio-format", "mp3"])
            elif extract_captions:
                cmd.extend(["--write-auto-sub", "--skip-download", "--sub-format", "vtt"])
            else:
                cmd.extend(["-f", f"bestvideo[ext={output_format}]+bestaudio/best[ext={output_format}]/best"])
            
            cmd.append(url)
            
            # Execute yt-dlp
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Find the output files
            files = {}
            base_name = os.path.basename(output_path)
            for file in os.listdir(work_dir):
                if file.startswith(base_name):
                    if extract_captions and file.endswith(".vtt"):
                        files["captions"] = os.path.join(work_dir, file)
                    elif extract_audio and file.endswith(".mp3"):
                        files["audio"] = os.path.join(work_dir, file)
                    elif file.endswith(f".{output_format}"):
                        files["video"] = os.path.join(work_dir, file)
            
            return {
                "success": True,
                "files": files,
                "format": output_format,
                "source_url": url
            }
        except Exception as e:
            return {"error": str(e)}




Day 4-5: Content Models and Storage

Define Content Data Models

Create Pydantic models for content representation:
python# api/models/content.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl

class ContentMetadata(BaseModel):
    """Metadata about the content."""
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    source_url: HttpUrl
    language: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class ContentBlock(BaseModel):
    """A block of content (paragraph, image, etc.)."""
    type: str  # "text", "image", "heading", "list", etc.
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Content(BaseModel):
    """Complete representation of extracted content."""
    id: Optional[str] = None
    metadata: ContentMetadata
    blocks: List[ContentBlock] = Field(default_factory=list)
    raw_content: Optional[str] = None
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
    
class ExtractionRequest(BaseModel):
    """Request model for content extraction."""
    url: HttpUrl
    include_images: bool = False
    max_depth: int = 1
    format: str = "markdown"  # "markdown", "text", "json"

class ExtractionResponse(BaseModel):
    """Response model for content extraction."""
    task_id: str
    status: str = "processing"
    message: Optional[str] = None



Set Up Content Storage

Create a simple content storage system using Modal volumes:
python# api/storage.py
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

class ContentStorage:
    """Simple storage for content using Modal volume."""
    
    def __init__(self, volume_path: str = "/data"):
        self.volume_path = volume_path
        os.makedirs(volume_path, exist_ok=True)
    
    def _get_content_path(self, content_id: str) -> str:
        """Get the path to the content file."""
        return os.path.join(self.volume_path, f"{content_id}.json")
    
    def save_content(self, content: Dict[str, Any]) -> str:
        """Save content to storage and return its ID."""
        content_id = content.get("id") or str(uuid.uuid4())
        content["id"] = content_id
        
        with open(self._get_content_path(content_id), "w") as f:
            json.dump(content, f)
        
        return content_id
    
    def get_content(self, content_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve content by ID."""
        path = self._get_content_path(content_id)
        if not os.path.exists(path):
            return None
        
        with open(path, "r") as f:
            return json.load(f)
    
    def list_contents(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List all contents with pagination."""
        files = [f for f in os.listdir(self.volume_path) if f.endswith(".json")]
        files.sort(reverse=True)  # Newest first
        
        page_files = files[offset:offset+limit]
        contents = []
        
        for file in page_files:
            with open(os.path.join(self.volume_path, file), "r") as f:
                contents.append(json.load(f))
        
        return contents
    
    def delete_content(self, content_id: str) -> bool:
        """Delete content by ID."""
        path = self._get_content_path(content_id)
        if not os.path.exists(path):
            return False
        
        os.remove(path)
        return True




Day 6-7: API Endpoint Development

Create Modal App with API Endpoints

Implement API endpoints for content extraction:
python# contentflow_api.py
import modal
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List

# Import extractors
from api.extractors.web_extractor import extract_web_content_sync
from api.extractors.media_extractor import extract_video_info, extract_video_content
from api.storage import ContentStorage

# Create Modal volume for storage
volume = modal.Volume.from_name(
    "contentflow-volume", 
    create_if_missing=True
)

# Define images with dependencies
base_image = modal.Image.debian_slim().pip_install(
    "fastapi>=0.95.0",
    "pydantic>=2.0.0"
)

web_image = base_image.pip_install(
    "crawl4ai>=0.5.0"
)

media_image = base_image.apt_install(
    "ffmpeg"
).pip_install(
    "yt-dlp>=2025.3.31"
)

# Create app
app = modal.App("contentflow-ai")

# Storage helper
@app.function(volumes={"/data": volume})
def storage_helper(operation: str, **kwargs) -> Dict[str, Any]:
    """Helper function to interact with storage."""
    storage = ContentStorage("/data")
    
    if operation == "save":
        content_id = storage.save_content(kwargs["content"])
        return {"content_id": content_id}
    elif operation == "get":
        content = storage.get_content(kwargs["content_id"])
        return {"content": content}
    elif operation == "list":
        contents = storage.list_contents(
            limit=kwargs.get("limit", 100),
            offset=kwargs.get("offset", 0)
        )
        return {"contents": contents}
    elif operation == "delete":
        success = storage.delete_content(kwargs["content_id"])
        return {"success": success}
    else:
        return {"error": f"Unknown operation: {operation}"}

# Web extraction endpoint
@app.function(image=web_image)
@modal.web_endpoint(method="POST")
def extract_web(url: str, include_images: bool = False, max_depth: int = 1):
    """Extract content from a web page."""
    task_id = str(uuid.uuid4())
    
    # Submit extraction job as a background task
    extract_web_background.spawn(
        task_id=task_id,
        url=url,
        include_images=include_images,
        max_depth=max_depth
    )
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": f"Extraction job submitted for {url}"
    }

# Background web extraction function
@app.function(
    image=web_image,
    volumes={"/data": volume},
    timeout=300
)
def extract_web_background(task_id: str, url: str, include_images: bool = False, max_depth: int = 1):
    """Background task to extract web content."""
    try:
        # Extract content
        content = extract_web_content_sync(url, include_images, max_depth)
        
        # Add metadata
        result = {
            "task_id": task_id,
            "status": "completed",
            "url": url,
            "content_type": "web",
            "extracted_at": datetime.utcnow().isoformat(),
            "data": content,
            "metadata": {
                "url": url,
                "include_images": include_images,
                "max_depth": max_depth
            }
        }
        
        # Save to storage
        storage = ContentStorage("/data")
        storage.save_content(result)
        
    except Exception as e:
        # Save error to storage
        error_data = {
            "task_id": task_id,
            "status": "failed",
            "url": url,
            "content_type": "web",
            "extracted_at": datetime.utcnow().isoformat(),
            "error": str(e),
            "metadata": {
                "url": url,
                "include_images": include_images,
                "max_depth": max_depth
            }
        }
        
        storage = ContentStorage("/data")
        storage.save_content(error_data)

# Video extraction endpoint
@app.function(image=media_image)
@modal.web_endpoint(method="POST")
def extract_video(url: str, format: str = "mp4", extract_audio: bool = False, extract_captions: bool = False):
    """Extract content from a video."""
    task_id = str(uuid.uuid4())
    
    # Submit extraction job as a background task
    extract_video_background.spawn(
        task_id=task_id,
        url=url,
        format=format,
        extract_audio=extract_audio,
        extract_captions=extract_captions
    )
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": f"Video extraction job submitted for {url}"
    }

# Background video extraction function
@app.function(
    image=media_image,
    volumes={"/data": volume},
    timeout=600
)
def extract_video_background(
    task_id: str, 
    url: str, 
    format: str = "mp4", 
    extract_audio: bool = False, 
    extract_captions: bool = False
):
    """Background task to extract video content."""
    try:
        # Get video info
        info = extract_video_info(url)
        
        # Extract content
        content = extract_video_content(
            url,
            output_format=format,
            extract_audio=extract_audio,
            extract_captions=extract_captions,
            temp_dir="/data"
        )
        
        # Add metadata
        result = {
            "task_id": task_id,
            "status": "completed",
            "url": url,
            "content_type": "video",
            "extracted_at": datetime.utcnow().isoformat(),
            "data": {
                "info": info,
                "content": content
            },
            "metadata": {
                "url": url,
                "format": format,
                "extract_audio": extract_audio,
                "extract_captions": extract_captions
            }
        }
        
        # Save to storage
        storage = ContentStorage("/data")
        storage.save_content(result)
        
    except Exception as e:
        # Save error to storage
        error_data = {
            "task_id": task_id,
            "status": "failed",
            "url": url,
            "content_type": "video",
            "extracted_at": datetime.utcnow().isoformat(),
            "error": str(e),
            "metadata": {
                "url": url,
                "format": format,
                "extract_audio": extract_audio,
                "extract_captions": extract_captions
            }
        }
        
        storage = ContentStorage("/data")
        storage.save_content(error_data)

# Task status endpoint
@app.function(volumes={"/data": volume})
@modal.web_endpoint()
def get_task_status(task_id: str):
    """Get the status of a task."""
    storage = ContentStorage("/data")
    content = storage.get_content(task_id)
    
    if not content:
        return {
            "task_id": task_id,
            "status": "not_found",
            "message": "Task not found or still processing"
        }
    
    return content

# List tasks endpoint
@app.function(volumes={"/data": volume})
@modal.web_endpoint()
def list_tasks(limit: int = 10, offset: int = 0):
    """List all tasks with pagination."""
    storage = ContentStorage("/data")
    contents = storage.list_contents(limit=limit, offset=offset)
    
    return {
        "count": len(contents),
        "tasks": contents
    }

# For local development
if __name__ == "__main__":
    app.serve()



Test API Endpoints

Create a simple test script:
python# test_api.py
import requests
import time
import json

# Replace with your actual Modal endpoint URLs
BASE_URL = "https://your-modal-app-url.modal.run"
EXTRACT_WEB_URL = f"{BASE_URL}/extract_web"
EXTRACT_VIDEO_URL = f"{BASE_URL}/extract_video"
GET_TASK_STATUS_URL = f"{BASE_URL}/get_task_status"

def test_web_extraction():
    """Test web extraction endpoint."""
    print("Testing web extraction...")
    
    # Send extraction request
    response = requests.post(
        EXTRACT_WEB_URL,
        params={
            "url": "https://www.example.com",
            "include_images": "false",
            "max_depth": "1"
        }
    )
    
    print(f"Response status: {response.status_code}")
    data = response.json()
    print(f"Response data: {json.dumps(data, indent=2)}")
    
    # Get task ID
    task_id = data.get("task_id")
    if not task_id:
        print("Error: No task ID returned")
        return
    
    # Poll for task status
    for _ in range(10):  # Try for up to 10 seconds
        print(f"Checking task status for {task_id}...")
        status_response = requests.get(
            GET_TASK_STATUS_URL,
            params={"task_id": task_id}
        )
        
        status_data = status_response.json()
        status = status_data.get("status")
        
        print(f"Task status: {status}")
        
        if status == "completed":
            print("Extraction completed successfully!")
            print(f"Extracted content: {json.dumps(status_data.get('data'), indent=2)}")
            return
        elif status == "failed":
            print(f"Extraction failed: {status_data.get('error')}")
            return
        
        # Wait before checking again
        time.sleep(1)
    
    print("Timed out waiting for extraction to complete")

if __name__ == "__main__":
    test_web_extraction()




Day 8-10: Content Processing Module

Design AI Transformation Module

Create module structure:
api/
├── processors/
│   ├── __init__.py
│   ├── summarizer.py       # Content summarization
│   ├── formatter.py        # Format adaptation
│   └── analyzer.py         # Content analysis



Implement Basic Summarization

Create a summarization function using Hugging Face models:
python# api/processors/summarizer.py
from typing import Dict, Any, List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

def load_summarization_model(model_name="Falconsai/text_summarization"):
    """Load a summarization model."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return pipeline("summarization", model=model, tokenizer=tokenizer)

def summarize_text(
    text: str,
    max_length: int = 150,
    min_length: int = 50,
    model_name: str = "Falconsai/text_summarization"
) -> Dict[str, Any]:
    """Summarize text using a pre-trained model."""
    try:
        # Check if text is too short
        if len(text.split()) < min_length:
            return {
                "summary": text,
                "model_used": model_name,
                "warning": "Text too short for summarization"
            }
        
        # Load model
        summarizer = load_summarization_model(model_name)
        
        # Split text into chunks if needed
        chunks = split_text_into_chunks(text, max_tokens=1000)
        
        # Summarize each chunk
        summaries = []
        for chunk in chunks:
            summary = summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            summaries.append(summary[0]["summary_text"])
        
        # Combine summaries if needed
        if len(summaries) > 1:
            combined_summary = " ".join(summaries)
            # Summarize again if combined summary is too long
            if len(combined_summary.split()) > max_length:
                combined_summary = summarizer(
                    combined_summary,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )[0]["summary_text"]
        else:
            combined_summary = summaries[0]
        
        return {
            "summary": combined_summary,
            "model_used": model_name,
            "chunks_processed": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}

def split_text_into_chunks(text: str, max_tokens: int = 1000) -> List[str]:
    """Split text into chunks respecting sentence boundaries."""
    sentences = text.split(". ")
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        # Rough estimate: 1 token per word
        sentence_length = len(sentence.split())
        
        if current_length + sentence_length > max_tokens:
            # Current chunk is full, start a new one
            chunks.append(". ".join(current_chunk) + ".")
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    # Add the last chunk
    if current_chunk:
        chunks.append(". ".join(current_chunk))
    
    return chunks



Implement Content Formatting

Create a formatting function for different platforms:
python# api/processors/formatter.py
from typing import Dict, Any, List, Optional

PLATFORM_FORMATS = {
    "twitter": {
        "max_length": 280,
        "supports_images": True,
        "supports_videos": True,
        "supports_links": True
    },
    "linkedin": {
        "max_length": 3000,
        "supports_images": True,
        "supports_videos": True,
        "supports_links": True
    },
    "instagram": {
        "max_length": 2200,
        "supports_images": True,
        "supports_videos": True,
        "supports_links": False  # Only in bio
    },
    "facebook": {
        "max_length": 63206,
        "supports_images": True,
        "supports_videos": True,
        "supports_links": True
    }
}

def format_for_platform(
    content: Dict[str, Any],
    platform: str,
    include_images: bool = True,
    include_links: bool = True,
    max_length: Optional[int] = None
) -> Dict[str, Any]:
    """Format content for a specific platform."""
    if platform not in PLATFORM_FORMATS:
        return {"error": f"Unknown platform: {platform}"}
    
    platform_format = PLATFORM_FORMATS[platform]
    
    # Get the text content
    text = content.get("text", "")
    if not text and "content" in content:
        text = content["content"]
    
    # Get metadata
    title = content.get("title", "")
    if not title and "metadata" in content and "title" in content["metadata"]:
        title = content["metadata"]["title"]
    
    description = content.get("description", "")
    if not description and "metadata" in content and "description" in content["metadata"]:
        description = content["metadata"]["description"]
    
    # Get links and images
    links = content.get("links", [])
    if not links and "metadata" in content and "links" in content["metadata"]:
        links = content["metadata"]["links"]
    
    images = content.get("images", [])
    if not images and "metadata" in content and "images" in content["metadata"]:
        images = content["metadata"]["images"]
    
    # Apply platform constraints
    max_content_length = max_length or platform_format["max_length"]
    
    # Format text for the platform
    formatted_text = text
    if len(formatted_text) > max_content_length:
        # Truncate text
        formatted_text = formatted_text[:max_content_length - 3] + "..."
    
    # Add title and description if there's space
    if title and len(title) + len(formatted_text) + 3 <= max_content_length:
        formatted_text = f"{title}\n\n{formatted_text}"
    
    # Handle links
    formatted_links = []
    if include_links and platform_format["supports_links"] and links:
        formatted_links = links[:3]  # Limit to top 3 links
    
    # Handle images
    formatted_images = []
    if include_images and platform_format["supports_images"] and images:
        formatted_images = images[:4]  # Limit to top 4 images
    
    return {
        "platform": platform,
        "text": formatted_text,
        "links": formatted_links,
        "images": formatted_images,
        "original_title": title,
        "original_description": description
    }




Day 11-12: Modal Integration for Content Processing

Create Modal App with Processing Endpoints

Implement endpoints for content summarization and formatting:
python# contentflow_processor.py
import modal
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List

# Import processors
from api.processors.summarizer import summarize_text
from api.processors.formatter import format_for_platform
from api.storage import ContentStorage

# Create Modal volume for storage
volume = modal.Volume.from_name(
    "contentflow-volume", 
    create_if_missing=True
)

# Define images with dependencies
processor_image = modal.Image.debian_slim().pip_install(
    "fastapi>=0.95.0",
    "pydantic>=2.0.0",
    "transformers>=4.34.0",
    "torch>=2.0.0"
)

# Create app
app = modal.App("contentflow-processor")

# Summarization endpoint
@app.function(
    image=processor_image,
    gpu="any"  # Use GPU for faster processing
)
@modal.web_endpoint(method="POST")
def summarize(text: str, max_length: int = 150, min_length: int = 50):
    """Summarize text using a pre-trained model."""
    result = summarize_



RetryClaude hit the max length for a message and has paused its response. You can write Continue to keep the chat going.BCcreate me a windsurfrules file for the project for my widsurf ideEditI'll create a comprehensive WindsurfRules file for your ContentFlow AI project that will define the code style, project structure, and development guidelines for your Windsurf IDE.WindsurfRules for ContentFlow AICode # WindsurfRules for ContentFlow AI Project

## Project Overview
- Project Name: ContentFlow AI
- Description: Intelligent content repurposing and automation platform
- Repository: https://github.com/yourusername/contentflow-ai
- Primary Technologies:I've created a comprehensive WindsurfRules file for your ContentFlow AI project, designed to provide clear guidance for your Windsurf IDE. This file establishes coding standards, project structure, and best practices for development.
The WindsurfRules file covers:

Project structure - Organized directory layout for backend, frontend, and infrastructure
Code style guidelines - For both Python and JavaScript/TypeScript
Modal Labs specific guidelines - Best practices for functions, volumes, and secrets
Testing standards - Unit and integration testing approaches
API design principles - RESTful conventions and request validation
Deployment processes - For both backend and frontend components
Git workflow - Branch strategy and commit message formatting
VSCode settings - Editor configurations for consistent development
Performance optimization - For API, Modal functions, and frontend
Security guidelines - Input validation and dependency management
Error handling and logging - Best practices for robust applications
Configuration management - Environment variable handling

This file will help ensure consistency across your development team and make your Windsurf IDE more effective at enforcing project standards. You can further customize it based on your specific project requirements and team preferences.RetryClaude can make mistakes. Please double-check responses. 3.7 Sonnet