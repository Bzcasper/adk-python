# app.py
import modal
import json
import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Union, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, File, UploadFile, Form, Body, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

# Create images with necessary dependencies
base_image = modal.Image.debian_slim().pip_install(
    "fastapi[standard]>=0.115.0",
    "pydantic>=2.0.0",
    "requests>=2.28.0",
    "beautifulsoup4>=4.11.0",
    "transformers>=4.37.0",
    "torch>=2.0.0",
    "pillow>=9.3.0"
)

# Add specialized crawl4ai image
crawl_image = base_image.pip_install(
    "crawl4ai>=0.5.0",
    "litellm>=0.6.0",
    "lxml>=4.9.0"
)

# Add video processing image with yt-dlp and ffmpeg
video_image = base_image.apt_install(
    "ffmpeg",
    "python3-dev",
    "gcc",
    "build-essential"
).pip_install(
    "yt-dlp>=2025.3.31",
    "pytubefix>=6.0.0"  # Alternative YouTube library as backup
)

# Create a Modal app
app = modal.App("content-extraction-service")

# Define secrets for API keys and authentication
app.secret = modal.Secret.from_name("api-keys")

# Shared storage for temporary processed data
volume = modal.Volume.from_name("extraction-volume", create_if_missing=True)

# Define request models
class WebExtractionRequest(BaseModel):
    url: str = Field(..., description="URL to extract content from")
    extract_type: str = Field("full_page", description="Type of extraction (full_page, article, headings)")
    format: str = Field("markdown", description="Output format (markdown, text, json)")
    max_length: Optional[int] = Field(None, description="Maximum length of extracted content")
    follow_links: bool = Field(False, description="Whether to follow links on the page")
    depth: int = Field(1, description="How many levels of links to follow")
    include_images: bool = Field(False, description="Whether to include images in the extraction")

class VideoExtractionRequest(BaseModel):
    url: str = Field(..., description="URL to the video to extract")
    extract_type: str = Field("audio", description="What to extract (audio, video, captions)")
    format: str = Field("mp3", description="Output format (mp3, mp4, txt)")
    quality: str = Field("best", description="Quality of the extracted content")
    start_time: Optional[str] = Field(None, description="Start time in format HH:MM:SS")
    end_time: Optional[str] = Field(None, description="End time in format HH:MM:SS")
    generate_transcript: bool = Field(False, description="Whether to generate a transcript")

class SummarizationRequest(BaseModel):
    content: str = Field(..., description="Content to summarize")
    max_length: int = Field(500, description="Maximum length of the summary")
    min_length: int = Field(100, description="Minimum length of the summary")
    model: str = Field("Falconsai/text_summarization", description="Hugging Face model to use")

class WebhookRegistrationRequest(BaseModel):
    callback_url: str = Field(..., description="URL to call when processing is complete")
    event_type: str = Field(..., description="Type of event to register for (extraction_complete, error)")
    headers: Optional[Dict[str, str]] = Field(None, description="Headers to include in the webhook call")

# Define response models
class ExtractionResponse(BaseModel):
    task_id: str
    status: str = "processing"
    message: str = "Extraction job submitted successfully"

class ExtractionResult(BaseModel):
    task_id: str
    status: str
    url: str
    content_type: str
    extracted_at: str
    data: Union[str, Dict[str, Any], List[Dict[str, Any]]]
    metadata: Dict[str, Any] = {}

# Auth handler using Bearer token
auth_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """Verify authentication token"""
    import os
    correct_token = os.environ.get("API_TOKEN")
    if not correct_token or credentials.credentials != correct_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Web extraction endpoint
@app.function(
    image=crawl_image,
    secrets=[app.secret],
    mounts=[modal.Mount.from_local_dir("./models", remote_path="/root/models")],
    timeout=300
)
@modal.fastapi_endpoint(method="POST")
async def extract_web_content(
    request: WebExtractionRequest,
    token: str = Depends(verify_token)
) -> ExtractionResponse:
    """
    Extract content from a webpage using crawl4ai
    """
    import uuid
    import time
    from datetime import datetime
    
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    
    # Submit the extraction job as a background task
    extract_web_content_task.spawn(
        task_id,
        request.url,
        request.extract_type,
        request.format,
        request.max_length,
        request.follow_links,
        request.depth,
        request.include_images
    )
    
    return ExtractionResponse(
        task_id=task_id,
        status="processing",
        message=f"Extraction job submitted for {request.url}"
    )

# Background web extraction function
@app.function(
    image=crawl_image,
    secrets=[app.secret],
    volumes={"/data": volume},
    timeout=600,
    keep_warm=1
)
def extract_web_content_task(
    task_id: str,
    url: str,
    extract_type: str = "full_page",
    format: str = "markdown",
    max_length: Optional[int] = None,
    follow_links: bool = False,
    depth: int = 1,
    include_images: bool = False
) -> None:
    """Background task to extract web content"""
    import asyncio
    import json
    import time
    from datetime import datetime
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
    from crawl4ai.extraction_strategy import MarkdownExtractionStrategy
    
    async def run_extraction():
        try:
            # Configure the browser
            browser_config = BrowserConfig(
                headless=True,
                ignore_https_errors=True,
                user_agent_type="desktop_chrome_latest"
            )
            
            # Configure the crawler based on extraction type
            crawler_config = CrawlerRunConfig(
                extraction_strategy=MarkdownExtractionStrategy(
                    include_images=include_images,
                    max_text_length=max_length if max_length else None
                ),
                follow_links=follow_links,
                max_links=50 if follow_links else 0,
                max_crawl_depth=depth if follow_links else 1
            )
            
            # Execute the crawl
            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url=url, config=crawler_config)
                
                # Process the result based on format
                if format == "markdown":
                    content = result.markdown.original_markdown
                elif format == "text":
                    content = result.markdown.to_text()
                elif format == "json":
                    content = {
                        "title": result.metadata.title,
                        "description": result.metadata.description,
                        "content": result.markdown.to_text(),
                        "links": result.links,
                        "images": result.images if include_images else []
                    }
                else:
                    content = result.markdown.original_markdown
                
                # Save result to volume
                result_data = {
                    "task_id": task_id,
                    "status": "completed",
                    "url": url,
                    "content_type": f"web_{extract_type}_{format}",
                    "extracted_at": datetime.now().isoformat(),
                    "data": content,
                    "metadata": {
                        "title": result.metadata.title,
                        "description": result.metadata.description,
                        "url": url,
                        "extraction_type": extract_type,
                        "format": format,
                        "links_followed": follow_links,
                        "depth": depth,
                        "images_included": include_images
                    }
                }
                
                with open(f"/data/{task_id}.json", "w") as f:
                    json.dump(result_data, f)
                
                # Here you would trigger a webhook if registered
                
        except Exception as e:
            # Save error to volume
            error_data = {
                "task_id": task_id,
                "status": "failed",
                "url": url,
                "content_type": f"web_{extract_type}_{format}",
                "extracted_at": datetime.now().isoformat(),
                "error": str(e),
                "metadata": {
                    "url": url,
                    "extraction_type": extract_type,
                    "format": format
                }
            }
            
            with open(f"/data/{task_id}.json", "w") as f:
                json.dump(error_data, f)
    
    # Run the extraction
    asyncio.run(run_extraction())

# Video extraction endpoint
@app.function(
    image=video_image,
    secrets=[app.secret],
    timeout=300
)
@modal.fastapi_endpoint(method="POST")
async def extract_video_content(
    request: VideoExtractionRequest,
    token: str = Depends(verify_token)
) -> ExtractionResponse:
    """
    Extract content from a video using yt-dlp
    """
    import uuid
    
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    
    # Submit the extraction job as a background task
    extract_video_content_task.spawn(
        task_id,
        request.url,
        request.extract_type,
        request.format,
        request.quality,
        request.start_time,
        request.end_time,
        request.generate_transcript
    )
    
    return ExtractionResponse(
        task_id=task_id,
        status="processing",
        message=f"Video extraction job submitted for {request.url}"
    )

# Background video extraction function
@app.function(
    image=video_image,
    secrets=[app.secret],
    volumes={"/data": volume},
    timeout=1200,
    keep_warm=1,
    cpu=2.0,
    memory=4096
)
def extract_video_content_task(
    task_id: str,
    url: str,
    extract_type: str = "audio",
    format: str = "mp3",
    quality: str = "best",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    generate_transcript: bool = False
) -> None:
    """Background task to extract video content"""
    import json
    import subprocess
    import tempfile
    import os
    from datetime import datetime
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, f"output.{format}")
            
            # Build yt-dlp command based on extraction type
            yt_dlp_cmd = ["yt-dlp"]
            
            # Format selection based on extraction type
            if extract_type == "audio":
                yt_dlp_cmd.extend(["-x", "--audio-format", format])
                if quality != "best":
                    yt_dlp_cmd.extend(["--audio-quality", quality])
            elif extract_type == "video":
                if format == "mp4":
                    yt_dlp_cmd.extend(["-f", f"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])
                else:
                    yt_dlp_cmd.extend(["-f", f"bestvideo+bestaudio/best"])
                    yt_dlp_cmd.extend(["--merge-output-format", format])
            elif extract_type == "captions":
                yt_dlp_cmd.extend(["--write-auto-sub", "--skip-download", "--sub-format", "vtt"])
                output_path = os.path.join(temp_dir, "output.vtt")
            
            # Add time parameters if provided
            if start_time and end_time:
                yt_dlp_cmd.extend(["--download-sections", f"*{start_time}-{end_time}"])
            
            # Add output path
            yt_dlp_cmd.extend(["-o", output_path, url])
            
            # Execute yt-dlp
            process = subprocess.run(
                yt_dlp_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            # Generate transcript if requested
            transcript = None
            if generate_transcript and extract_type in ["audio", "video"]:
                try:
                    from transformers import pipeline
                    transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")
                    transcript = transcriber(output_path)["text"]
                except Exception as e:
                    transcript = f"Transcription failed: {str(e)}"
            
            # Move the output file to the volume
            final_output_path = f"/data/{task_id}.{format}"
            if os.path.exists(output_path):
                with open(output_path, "rb") as src, open(final_output_path, "wb") as dst:
                    dst.write(src.read())
            
            # Save result metadata
            result_data = {
                "task_id": task_id,
                "status": "completed",
                "url": url,
                "content_type": f"video_{extract_type}_{format}",
                "extracted_at": datetime.now().isoformat(),
                "data": {
                    "file_path": final_output_path,
                    "transcript": transcript
                },
                "metadata": {
                    "url": url,
                    "extraction_type": extract_type,
                    "format": format,
                    "quality": quality,
                    "start_time": start_time,
                    "end_time": end_time,
                    "transcript_generated": generate_transcript
                }
            }
            
            with open(f"/data/{task_id}.json", "w") as f:
                json.dump(result_data, f)
                
    except Exception as e:
        # Save error to volume
        error_data = {
            "task_id": task_id,
            "status": "failed",
            "url": url,
            "content_type": f"video_{extract_type}_{format}",
            "extracted_at": datetime.now().isoformat(),
            "error": str(e),
            "metadata": {
                "url": url,
                "extraction_type": extract_type,
                "format": format
            }
        }
        
        with open(f"/data/{task_id}.json", "w") as f:
            json.dump(error_data, f)

# Text summarization endpoint
@app.function(
    image=base_image,
    secrets=[app.secret],
    gpu="any",
    timeout=300
)
@modal.fastapi_endpoint(method="POST")
async def summarize_text(
    request: SummarizationRequest,
    token: str = Depends(verify_token)
) -> Dict[str, Any]:
    """
    Summarize text using Hugging Face models
    """
    from transformers import pipeline
    import torch
    
    try:
        # Initialize the summarization pipeline
        summarizer = pipeline(
            "summarization", 
            model=request.model,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Generate summary
        summary = summarizer(
            request.content,
            max_length=request.max_length,
            min_length=request.min_length,
            do_sample=False
        )
        
        return {
            "status": "success",
            "summary": summary[0]["summary_text"],
            "model_used": request.model,
            "input_length": len(request.content),
            "output_length": len(summary[0]["summary_text"])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )

# Get task status endpoint
@app.function(
    image=base_image,
    volumes={"/data": volume},
    keep_warm=1
)
@modal.fastapi_endpoint()
async def get_task_status(
    task_id: str,
    token: str = Depends(verify_token)
) -> Dict[str, Any]:
    """
    Get the status of a task
    """
    import json
    import os
    
    task_file = f"/data/{task_id}.json"
    
    if not os.path.exists(task_file):
        return {
            "task_id": task_id,
            "status": "not_found",
            "message": "Task not found or still processing"
        }
    
    try:
        with open(task_file, "r") as f:
            task_data = json.load(f)
        
        return task_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving task status: {str(e)}"
        )

# Register webhook endpoint
@app.function(
    image=base_image,
    secrets=[app.secret],
    keep_warm=1
)
@modal.fastapi_endpoint(method="POST")
async def register_webhook(
    request: WebhookRegistrationRequest,
    token: str = Depends(verify_token)
) -> Dict[str, Any]:
    """
    Register a webhook for event notifications
    """
    import uuid
    
    webhook_id = str(uuid.uuid4())
    
    # Here you would store the webhook registration in a database
    # For simplicity, we'll just return success
    
    return {
        "webhook_id": webhook_id,
        "status": "registered",
        "callback_url": request.callback_url,
        "event_type": request.event_type,
        "message": "Webhook registered successfully"
    }

# Main entrypoint for local development
@app.local_entrypoint()
def main():
    print("Content Extraction API is ready for deployment")
    print("To deploy: modal deploy app.py")
    print("For local testing: modal serve app.py")
