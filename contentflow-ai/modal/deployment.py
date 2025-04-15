"""Modal Labs deployment configuration for ContentFlow AI.

This module defines the Modal Labs deployment configuration for the ContentFlow AI
platform, including the container image, GPU requirements, and API endpoints.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
from src.agents.extraction.audio_extraction_agent import AudioExtractionAgent

try:
    import modal
except ImportError:
    print("Modal package not found. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "modal"])
    import modal

# Define the Modal stub for ContentFlow AI
stub = modal.Stub(
    "contentflow-ai",
    image=None,  # We'll define the image below
    secrets=[modal.Secret.from_name("contentflow-api-keys") if os.getenv("MODAL_ENVIRONMENT") == "production" else None],
)

# Define the base image with all dependencies
image = modal.Image.debian_slim().pip_install([
    "google-adk>=0.1.0",
    "crawl4ai==0.5",
    "yt-dlp>=2023.3.4",
    "ffmpeg-python>=0.2.0",
    "pydantic>=2.0.0,<3.0.0",
    "fastapi>=0.115.0",
    "uvicorn>=0.34.0",
    "python-multipart>=0.0.9",
    "transformers>=4.38.0",
    "torch>=2.2.0",
    "numpy>=1.26.0",
    "pandas>=2.2.0",
    "pillow>=10.2.0",
    "python-dotenv>=1.0.0",
    "modal>=0.55.4",
])

# Update the stub with the image
stub.image = image

# Create a volume for persistent storage
content_volume = modal.Volume.from_name("contentflow-content", create_if_missing=True)

# Environment variables
env = {
    "PYTHONPATH": "/app",
    "LOG_LEVEL": "INFO",
    "DEPLOYMENT_TIMESTAMP": datetime.now().isoformat(),
}

# Import our ContentFlow AI agents and tools
from src.agents.extraction.web_content_agent import WebContentAgent
from src.agents.extraction.video_download_agent import VideoDownloadAgent
from src.agents.transformation.text_transformation_agent import TextTransformationAgent
from src.models.serving.vllm_service import vllm_stub, vllm_app, download_model, generate_text

# Define the health check endpoint
@stub.function(
    volumes={"/app/data": content_volume},
    env=env,
    timeout=60,
)
@modal.fastapi_endpoint(method="GET")
async def health():
    """Health check endpoint for the ContentFlow AI API."""
    return {
        "status": "healthy", 
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }

# Define the extraction function with GPU access
@stub.function(
    volumes={"/app/data": content_volume},
    env=env,
    timeout=300,
    gpu="A100",  # Using A100 GPU for extraction tasks
    memory=8192,  # 8GB memory allocation
    retries=3,    # Retry up to 3 times on failure
)
async def extract_content(url: str, content_type: str = "article") -> Dict[str, Any]:
    """
    Extract content from a URL using the appropriate extraction agent.
    
    Args:
        url: The URL to extract content from.
        content_type: The type of content to extract (article, video, etc.).
        
    Returns:
        A dictionary containing the extracted content and metadata.
    """
    try:
        # Initialize the appropriate agent based on content type
        if content_type == "article" or content_type == "web":
            agent = WebContentAgent(model="gemini-2.0-pro")
            return await agent.extract_article(url)
        elif content_type == "video":
            agent = VideoDownloadAgent(model="gemini-2.0-pro")
            # First extract metadata to get information about the video
            metadata = await agent.extract_video_metadata(url)
            # Then extract the transcript if available
            try:
                transcript = await agent.extract_video_transcript(url)
                metadata["transcript"] = transcript["transcript"]
                metadata["transcript_segments"] = transcript["segments"]
            except Exception as e:
                print(f"Error extracting transcript: {str(e)}")
                metadata["transcript"] = "Transcript not available"
            
            return metadata
        elif content_type == "audio":
            # For audio extraction, we need a video path
            # In a real implementation, we would download the video first
            # and then extract the audio
            video_path = f"/tmp/{url.split('/')[-1]}"
            agent = AudioExtractionAgent(model="gemini-2.0-pro")
            
            # Extract audio from the video
            audio_result = await agent.extract_audio(
                video_path=video_path,
                audio_format="mp3",
                quality="high"
            )
            
            # Analyze the audio content
            try:
                audio_analysis = await agent.analyze_audio_content(
                    audio_path=audio_result["output_path"]
                )
                audio_result["analysis"] = audio_analysis
            except Exception as e:
                print(f"Error analyzing audio: {str(e)}")
                audio_result["analysis"] = "Audio analysis not available"
            
            return audio_result
        else:
            return {
                "url": url,
                "error": f"Unsupported content type: {content_type}",
            }
    except Exception as e:
        # Log the error and return a structured error response
        print(f"Error extracting content from {url}: {str(e)}")
        return {
            "url": url,
            "error": str(e),
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }

# Define the transformation function with GPU access
@stub.function(
    volumes={"/app/data": content_volume},
    env=env,
    timeout=300,
    gpu="A100",  # Using A100 GPU for transformation tasks
    memory=8192,  # 8GB memory allocation
    retries=3,    # Retry up to 3 times on failure
)
async def transform_content(
    content: Dict[str, Any],
    target_format: str,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Transform content from one format to another using the appropriate transformation agent.
    
    Args:
        content: The content to transform.
        target_format: The target format for the transformation.
        options: Optional transformation options.
        
    Returns:
        A dictionary containing the transformed content and metadata.
    """
    try:
        # Initialize the appropriate transformation agent based on the content type
        content_type = content.get("content_type", "unknown")
        
        if content_type == "article" or content_type == "text":
            # Use the TextTransformationAgent for text content
            agent = TextTransformationAgent(
                model="gemini-2.0-pro",
                vllm_model=options.get("vllm_model", "mistral-7b")
            )
            
            # Get the text content
            text = content.get("content", "")
            if not text and "text" in content:
                text = content["text"]
            elif not text and "body" in content:
                text = content["body"]
            elif not text and "html" in content:
                text = content["html"]
                
            # Transform the text based on the target format
            if target_format == "summary":
                result = await agent.summarize_text(
                    text=text,
                    max_length=options.get("max_length", 500),
                    style=options.get("style", "informative"),
                    format=options.get("format", "paragraph")
                )
                return {
                    "status": "success",
                    "content_id": content.get("id", str(uuid.uuid4())),
                    "original_format": content_type,
                    "target_format": target_format,
                    "options": options or {},
                    "transformed_content": result,
                    "timestamp": datetime.now().isoformat(),
                }
            elif target_format == "style_transfer":
                result = await agent.change_style(
                    text=text,
                    target_style=options.get("target_style", "formal"),
                    preserve_meaning=options.get("preserve_meaning", True),
                    format=options.get("format", "paragraph")
                )
                return {
                    "status": "success",
                    "content_id": content.get("id", str(uuid.uuid4())),
                    "original_format": content_type,
                    "target_format": target_format,
                    "options": options or {},
                    "transformed_content": result,
                    "timestamp": datetime.now().isoformat(),
                }
            elif target_format in ["markdown", "html", "json", "text"]:
                result = await agent.convert_format(
                    text=text,
                    target_format=target_format,
                    preserve_content=options.get("preserve_content", True),
                    add_metadata=options.get("add_metadata", False)
                )
                return {
                    "status": "success",
                    "content_id": content.get("id", str(uuid.uuid4())),
                    "original_format": content_type,
                    "target_format": target_format,
                    "options": options or {},
                    "transformed_content": result,
                    "timestamp": datetime.now().isoformat(),
                }
            else:
                return {
                    "status": "failed",
                    "error": f"Unsupported target format: {target_format}",
                    "content_id": content.get("id", str(uuid.uuid4())),
                    "original_format": content_type,
                    "target_format": target_format,
                    "timestamp": datetime.now().isoformat(),
                }
        else:
            # For other content types, return a placeholder result
            # In a real implementation, we would use the appropriate transformation agent
            return {
                "status": "failed",
                "error": f"Unsupported content type: {content_type}",
                "content_id": content.get("id", str(uuid.uuid4())),
                "original_format": content_type,
                "target_format": target_format,
                "timestamp": datetime.now().isoformat(),
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "content_id": content.get("id", "unknown"),
            "target_format": target_format,
            "timestamp": datetime.now().isoformat(),
        }

# Define the main API app using FastAPI
@stub.function(
    volumes={"/app/data": content_volume},
    env=env,
    timeout=300,
    concurrency_limit=10,  # Limit concurrent requests
)
@modal.fastapi_endpoint()
def api():
    """Main API endpoint for the ContentFlow AI platform."""
    from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse, JSONResponse
    from pydantic import BaseModel, Field, HttpUrl
    import time
    import uuid
    
    # Create FastAPI app with documentation
    app = FastAPI(
        title="ContentFlow AI API",
        description="Intelligent content repurposing and automation platform API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Add CORS middleware to allow cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Define request and response models using Pydantic
    class ExtractionRequest(BaseModel):
        url: HttpUrl = Field(..., description="URL to extract content from")
        content_type: str = Field(default="article", description="Type of content to extract (article, video, etc.)")
    
    class TransformationRequest(BaseModel):
        content: Dict[str, Any] = Field(..., description="Content to transform")
        target_format: str = Field(..., description="Target format for the transformation")
        options: Optional[Dict[str, Any]] = Field(default=None, description="Optional transformation options")
    
    # Add middleware for request timing and logging
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state for logging
        request.state.request_id = request_id
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            process_time = time.time() - start_time
            return JSONResponse(
                status_code=500,
                content={
                    "detail": str(e),
                    "request_id": request_id,
                    "process_time": process_time
                }
            )
    class AudioExtractionRequest(BaseModel):
        url: HttpUrl = Field(..., description="URL of the video to extract audio from")
        audio_format: str = Field(default="mp3", description="Format of the extracted audio")
        quality: str = Field(default="high", description="Quality of the extracted audio")
    
    class AudioAnalysisRequest(BaseModel):
        url: HttpUrl = Field(..., description="URL of the video to analyze audio from")
    
    class TransformationRequest(BaseModel):
        content: Dict[str, Any] = Field(..., description="Content to transform")
        target_format: str = Field(..., description="Target format for the transformation")
        options: Optional[Dict[str, Any]] = Field(default=None, description="Optional transformation options")
    
    # Define Pydantic models for vLLM model serving
    class ModelInfoResponse(BaseModel):
        model_id: str = Field(..., description="The unique identifier for the model")
        model_name: str = Field(..., description="The name of the model")
        model_family: str = Field(..., description="The family the model belongs to (e.g., Mistral, Llama)")
        provider: str = Field(..., description="The provider of the model (e.g., HuggingFace, Meta)")
        parameters: Dict[str, Any] = Field(..., description="Model parameters and configuration")
        description: str = Field(..., description="A description of the model")
        license: str = Field(..., description="The license of the model")
        commercial_use: bool = Field(..., description="Whether the model is suitable for commercial use")
        status: str = Field(..., description="The status of the model (e.g., ready, downloading)")
        last_updated: str = Field(..., description="When the model was last updated")
    
    class TextGenerationRequest(BaseModel):
        prompt: str = Field(..., description="The prompt to generate text from")
        model_name: str = Field(default="mistral-7b", description="The name of the model to use")
        max_tokens: int = Field(default=512, description="The maximum number of tokens to generate")
        temperature: float = Field(default=0.7, description="The temperature to use for sampling")
        top_p: float = Field(default=0.9, description="The top-p value to use for sampling")
        top_k: int = Field(default=50, description="The top-k value to use for sampling")
        repetition_penalty: float = Field(default=1.1, description="Penalty for repetition")
        use_torch_compile: bool = Field(default=True, description="Whether to use torch.compile for optimization")
        stream: bool = Field(default=False, description="Whether to stream the response")
        
        class Config:
            schema_extra = {
                "example": {
                    "prompt": "Write a short story about a robot learning to paint.",
                    "model_name": "mistral-7b",
                    "max_tokens": 512,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1,
                    "use_torch_compile": True,
                    "stream": False
                }
            }
    
    class TextGenerationResponse(BaseModel):
        status: str = Field(..., description="The status of the request")
        model_name: str = Field(..., description="The name of the model used")
        model_id: str = Field(..., description="The unique identifier for the model")
        prompt: str = Field(..., description="The prompt used for generation")
        generated_text: str = Field(..., description="The generated text")
        load_time: float = Field(..., description="Time taken to load the model in seconds")
        generation_time: float = Field(..., description="Time taken to generate the text in seconds")
        total_time: float = Field(..., description="Total time taken for the request in seconds")
        timestamp: str = Field(..., description="When the request was processed")
        parameters: Dict[str, Any] = Field(..., description="The parameters used for generation")
    
    # Define API routes
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to ContentFlow AI API",
            "version": "0.1.0",
            "documentation": "/docs"
        }
    
    @app.post("/extract", summary="Extract content from a URL")
    async def extract(request: ExtractionRequest):
        try:
            result = await extract_content.remote(str(request.url), request.content_type)
            if "error" in result and "status" in result and result["status"] == "failed":
                raise HTTPException(status_code=500, detail=result["error"])
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "url": str(request.url),
                    "content_type": request.content_type
                }
            )
    
    @app.post("/extract/audio", summary="Extract audio from a video URL")
    async def extract_audio_endpoint(request: AudioExtractionRequest):
        """Extract audio from a video URL."""
        try:
            # Use the extract_content function with content_type="audio"
            result = await extract_content.remote(str(request.url), "audio")
            if "error" in result and "status" in result and result["status"] == "failed":
                raise HTTPException(status_code=500, detail=result["error"])
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "url": str(request.url),
                    "audio_format": request.audio_format,
                    "quality": request.quality
                }
            )
    
    @app.post("/analyze/audio", summary="Analyze audio content from a video URL")
    async def analyze_audio_endpoint(request: AudioAnalysisRequest):
        """Analyze audio content from a video URL."""
        try:
            # First extract the audio
            audio_result = await extract_content.remote(str(request.url), "audio")
            
            # Then get the analysis from the result
            if isinstance(audio_result.get("analysis"), dict):
                return audio_result["analysis"]
            else:
                return {
                    "url": str(request.url),
                    "error": "Audio analysis not available",
                    "status": "failed",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "url": str(request.url)
                }
            )
    
    @app.post("/transform", summary="Transform content to a different format")
    async def transform(request: TransformationRequest):
        try:
            result = await transform_content.remote(
                request.content,
                request.target_format,
                request.options
            )
            if "error" in result and "status" in result and result["status"] == "failed":
                raise HTTPException(status_code=500, detail=result["error"])
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "target_format": request.target_format
                }
            )
    
    # Health check endpoint
    @app.get("/health", summary="Health check endpoint")
    async def api_health():
        return {
            "status": "healthy",
            "version": "0.1.0",
            "timestamp": datetime.now().isoformat()
        }
    
    # vLLM Model Serving Endpoints
    @app.get("/models", summary="List available models")
    async def list_models():
        """List all available models for text generation."""
        try:
            # Define the available models with their information
            models = {
                "mistral-7b": {
                    "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
                    "model_name": "mistral-7b",
                    "model_family": "Mistral",
                    "provider": "MistralAI",
                    "parameters": {
                        "parameters": 7.3,  # Billion parameters
                        "context_window": 8192,
                        "architecture": "Transformer",
                    },
                    "description": "Mistral 7B Instruct v0.2 is a state-of-the-art instruction-tuned model based on Mistral 7B.",
                    "license": "Apache 2.0",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
                "llama3-8b": {
                    "model_id": "meta-llama/Meta-Llama-3-8B-Instruct",
                    "model_name": "llama3-8b",
                    "model_family": "Llama",
                    "provider": "Meta",
                    "parameters": {
                        "parameters": 8.0,  # Billion parameters
                        "context_window": 8192,
                        "architecture": "Transformer",
                    },
                    "description": "Meta Llama 3 8B Instruct is a state-of-the-art instruction-tuned model from Meta AI.",
                    "license": "Meta Llama 3 Community License",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
                "phi3-14b": {
                    "model_id": "microsoft/Phi-3-medium-4k-instruct",
                    "model_name": "phi3-14b",
                    "model_family": "Phi",
                    "provider": "Microsoft",
                    "parameters": {
                        "parameters": 14.0,  # Billion parameters
                        "context_window": 4096,
                        "architecture": "Transformer",
                    },
                    "description": "Microsoft Phi-3 Medium is a state-of-the-art instruction-tuned model from Microsoft.",
                    "license": "MIT",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
                "gemma-7b": {
                    "model_id": "google/gemma-7b-it",
                    "model_name": "gemma-7b",
                    "model_family": "Gemma",
                    "provider": "Google",
                    "parameters": {
                        "parameters": 7.0,  # Billion parameters
                        "context_window": 8192,
                        "architecture": "Transformer",
                    },
                    "description": "Google Gemma 7B Instruct is a state-of-the-art instruction-tuned model from Google.",
                    "license": "Gemma License",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
            }
            return {"models": models}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "message": "Failed to list models"
                }
            )
    
    @app.get("/models/{model_name}", summary="Get model information", response_model=ModelInfoResponse)
    async def get_model_info(model_name: str):
        """Get information about a specific model."""
        try:
            # Define the available models with their information
            models = {
                "mistral-7b": {
                    "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
                    "model_name": "mistral-7b",
                    "model_family": "Mistral",
                    "provider": "MistralAI",
                    "parameters": {
                        "parameters": 7.3,  # Billion parameters
                        "context_window": 8192,
                        "architecture": "Transformer",
                    },
                    "description": "Mistral 7B Instruct v0.2 is a state-of-the-art instruction-tuned model based on Mistral 7B.",
                    "license": "Apache 2.0",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
                "llama3-8b": {
                    "model_id": "meta-llama/Meta-Llama-3-8B-Instruct",
                    "model_name": "llama3-8b",
                    "model_family": "Llama",
                    "provider": "Meta",
                    "parameters": {
                        "parameters": 8.0,  # Billion parameters
                        "context_window": 8192,
                        "architecture": "Transformer",
                    },
                    "description": "Meta Llama 3 8B Instruct is a state-of-the-art instruction-tuned model from Meta AI.",
                    "license": "Meta Llama 3 Community License",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
                "phi3-14b": {
                    "model_id": "microsoft/Phi-3-medium-4k-instruct",
                    "model_name": "phi3-14b",
                    "model_family": "Phi",
                    "provider": "Microsoft",
                    "parameters": {
                        "parameters": 14.0,  # Billion parameters
                        "context_window": 4096,
                        "architecture": "Transformer",
                    },
                    "description": "Microsoft Phi-3 Medium is a state-of-the-art instruction-tuned model from Microsoft.",
                    "license": "MIT",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
                "gemma-7b": {
                    "model_id": "google/gemma-7b-it",
                    "model_name": "gemma-7b",
                    "model_family": "Gemma",
                    "provider": "Google",
                    "parameters": {
                        "parameters": 7.0,  # Billion parameters
                        "context_window": 8192,
                        "architecture": "Transformer",
                    },
                    "description": "Google Gemma 7B Instruct is a state-of-the-art instruction-tuned model from Google.",
                    "license": "Gemma License",
                    "commercial_use": True,
                    "status": "ready",
                    "last_updated": "2024-04-15T00:00:00.000000",
                },
            }
            
            if model_name not in models:
                raise HTTPException(
                    status_code=404,
                    detail=f"Model '{model_name}' not found. Available models: {list(models.keys())}"
                )
                
            return models[model_name]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "message": f"Failed to get information for model '{model_name}'"
                }
            )
    
    @app.post("/models/generate", summary="Generate text using a model", response_model=TextGenerationResponse)
    async def generate_text_endpoint(request: TextGenerationRequest):
        """Generate text using a specified model."""
        try:
            # Call the vLLM service to generate text
            result = await generate_text.remote(
                prompt=request.prompt,
                model_name=request.model_name,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k,
                repetition_penalty=request.repetition_penalty,
                use_torch_compile=request.use_torch_compile,
            )
            
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "message": "Failed to generate text",
                    "model": request.model_name
                }
            )
    
    @app.post("/models/download/{model_name}", summary="Download a model")
    async def download_model_endpoint(model_name: str, background_tasks: BackgroundTasks):
        """Download a model for use with vLLM."""
        try:
            # Map model_name to model_id
            model_ids = {
                "mistral-7b": "mistralai/Mistral-7B-Instruct-v0.2",
                "llama3-8b": "meta-llama/Meta-Llama-3-8B-Instruct",
                "phi3-14b": "microsoft/Phi-3-medium-4k-instruct",
                "gemma-7b": "google/gemma-7b-it",
            }
            
            if model_name not in model_ids:
                raise HTTPException(
                    status_code=404,
                    detail=f"Model '{model_name}' not found. Available models: {list(model_ids.keys())}"
                )
            
            # Start downloading the model in the background
            background_tasks.add_task(
                download_model.remote,
                model_id=model_ids[model_name],
                model_name=model_name
            )
            
            return {
                "status": "downloading",
                "model_name": model_name,
                "model_id": model_ids[model_name],
                "message": f"Started downloading model '{model_name}'. This may take several minutes.",
                "timestamp": datetime.now().isoformat()
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "message": f"Failed to download model '{model_name}'"
                }
            )
    
    return app
