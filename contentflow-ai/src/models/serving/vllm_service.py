"""High-performance model serving using vLLM and torch.compile.

This module provides high-performance model serving capabilities for ContentFlow AI
using vLLM for efficient inference and torch.compile for optimized performance.
It follows Modal Labs best practices for serverless deployment.
"""

import os
import time
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import packaging.version

try:
    import modal
except ImportError:
    print("Modal package not found. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "modal"])
    import modal
import torch
from vllm import LLM, SamplingParams
from pydantic import BaseModel, Field

# Define the Modal stub for vLLM model serving
vllm_stub = modal.Stub("contentflow-ai-vllm")

# Create a volume to store downloaded models
model_volume = modal.Volume.from_name(
    "contentflow-ai-models", 
    create_if_missing=True
)

# Define the available models
AVAILABLE_MODELS = {
    "mistral-7b": {
        "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
        "description": "Mistral 7B Instruct v0.2 - A powerful instruction-tuned model",
        "context_length": 8192,
        "commercial_use": True,
    },
    "llama3-8b": {
        "model_id": "meta-llama/Meta-Llama-3-8B-Instruct",
        "description": "Meta Llama 3 8B Instruct - Meta's latest open-source model",
        "context_length": 8192,
        "commercial_use": True,
    },
    "phi3-14b": {
        "model_id": "microsoft/Phi-3-medium-4k-instruct",
        "description": "Microsoft Phi-3 Medium (14B) - Efficient and powerful instruction model",
        "context_length": 4096,
        "commercial_use": True,
    },
    "gemma-7b": {
        "model_id": "google/gemma-7b-it",
        "description": "Google Gemma 7B Instruct - Google's efficient instruction model",
        "context_length": 8192,
        "commercial_use": True,
    },
}

# Define the default model to use
DEFAULT_MODEL = "mistral-7b"

# Define the vLLM image with all dependencies
vllm_image = modal.Image.debian_slim().pip_install([
    "vllm>=0.3.0",
    "torch>=2.2.0",
    "transformers>=4.38.0",
    "accelerate>=0.27.0",
    "pydantic>=2.0.0,<3.0.0",
    "fastapi>=0.115.0",
    "uvicorn>=0.34.0",
    "safetensors>=0.4.0",
])

# Environment variables
env = {
    "PYTHONPATH": "/app",
    "LOG_LEVEL": "INFO",
    "DEPLOYMENT_TIMESTAMP": datetime.now().isoformat(),
}


@vllm_stub.function(
    image=vllm_image,
    gpu="A100",
    timeout=600,
    volumes={"/models": model_volume},
    env=env,
)
def download_model(model_name: str) -> Dict[str, Any]:
    """
    Download a model and save it to the model volume.
    
    Args:
        model_name: The name of the model to download.
        
    Returns:
        A dictionary containing information about the downloaded model.
    """
    from huggingface_hub import snapshot_download
    import os
    
    if model_name not in AVAILABLE_MODELS:
        return {
            "status": "error",
            "message": f"Model {model_name} not found. Available models: {list(AVAILABLE_MODELS.keys())}",
            "timestamp": datetime.now().isoformat(),
        }
    
    model_info = AVAILABLE_MODELS[model_name]
    model_id = model_info["model_id"]
    
    # Create the model directory if it doesn't exist
    model_dir = f"/models/{model_name}"
    os.makedirs(model_dir, exist_ok=True)
    
    # Download the model
    print(f"Downloading model {model_id} to {model_dir}...")
    start_time = time.time()
    
    snapshot_download(
        repo_id=model_id,
        local_dir=model_dir,
        local_dir_use_symlinks=False,
    )
    
    download_time = time.time() - start_time
    print(f"Model {model_id} downloaded in {download_time:.2f} seconds")
    
    # Create a metadata file
    metadata = {
        "model_id": model_id,
        "model_name": model_name,
        "description": model_info["description"],
        "context_length": model_info["context_length"],
        "commercial_use": model_info["commercial_use"],
        "download_time": download_time,
        "download_timestamp": datetime.now().isoformat(),
    }
    
    with open(f"{model_dir}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    return {
        "status": "success",
        "model_name": model_name,
        "model_id": model_id,
        "model_dir": model_dir,
        "download_time": download_time,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata,
    }


@vllm_stub.function(
    image=vllm_image,
    gpu="A100",
    timeout=60,
    volumes={"/models": model_volume},
    env=env,
    concurrency_limit=2,  # Limit concurrent requests to avoid OOM
)
async def generate_text(
    prompt: str,
    model_name: str = DEFAULT_MODEL,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 50,
    repetition_penalty: float = 1.1,
    use_torch_compile: bool = True,
) -> Dict[str, Any]:
    """
    Generate text using vLLM with the specified model.
    
    Args:
        prompt: The prompt to generate text from.
        model_name: The name of the model to use.
        max_tokens: The maximum number of tokens to generate.
        temperature: The temperature to use for sampling.
        top_p: The top-p value to use for sampling.
        top_k: The top-k value to use for sampling.
        repetition_penalty: The repetition penalty to apply.
        use_torch_compile: Whether to use torch.compile for optimized performance.
        
    Returns:
        A dictionary containing the generated text and metadata.
    """
    if model_name not in AVAILABLE_MODELS:
        return {
            "status": "error",
            "message": f"Model {model_name} not found. Available models: {list(AVAILABLE_MODELS.keys())}",
            "timestamp": datetime.now().isoformat(),
        }
    
    model_dir = f"/models/{model_name}"
    
    # Check if the model is downloaded
    if not os.path.exists(model_dir):
        return {
            "status": "error",
            "message": f"Model {model_name} not downloaded. Please download it first.",
            "timestamp": datetime.now().isoformat(),
        }
    
    # Load the model metadata
    with open(f"{model_dir}/metadata.json", "r") as f:
        metadata = json.load(f)
    
    # Set up the sampling parameters
    sampling_params = SamplingParams(
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        repetition_penalty=repetition_penalty,
    )
    
    # Initialize the vLLM model
    print(f"Loading model {model_name} from {model_dir}...")
    start_time = time.time()
    
    # Use torch.compile if requested
    if use_torch_compile and packaging.version.parse(torch.__version__) >= packaging.version.parse("2.0.0"):
        print("Using torch.compile for optimized performance")
        torch._dynamo.config.suppress_errors = True
        
        # Define a compiled model loader
        def load_compiled_model():
            llm = LLM(
                model=model_dir,
                tensor_parallel_size=1,  # Use all available GPUs
                trust_remote_code=True,
                max_model_len=metadata["context_length"],
            )
            # Compile the model's forward pass
            llm.model.forward = torch.compile(
                llm.model.forward,
                mode="reduce-overhead",
                fullgraph=True,
            )
            return llm
        
        llm = load_compiled_model()
    else:
        llm = LLM(
            model=model_dir,
            tensor_parallel_size=1,  # Use all available GPUs
            trust_remote_code=True,
            max_model_len=metadata["context_length"],
        )
    
    load_time = time.time() - start_time
    print(f"Model {model_name} loaded in {load_time:.2f} seconds")
    
    # Generate text
    print(f"Generating text for prompt: {prompt[:50]}...")
    start_time = time.time()
    
    outputs = llm.generate([prompt], sampling_params)
    
    generation_time = time.time() - start_time
    print(f"Text generated in {generation_time:.2f} seconds")
    
    # Extract the generated text
    generated_text = outputs[0].outputs[0].text
    
    return {
        "status": "success",
        "model_name": model_name,
        "model_id": metadata["model_id"],
        "prompt": prompt,
        "generated_text": generated_text,
        "load_time": load_time,
        "generation_time": generation_time,
        "total_time": load_time + generation_time,
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repetition_penalty": repetition_penalty,
            "use_torch_compile": use_torch_compile,
        },
    }


# Define the FastAPI app for model serving
@vllm_stub.function(
    image=vllm_image,
    volumes={"/models": model_volume},
    env=env,
    timeout=600,
    concurrency_limit=10,
)
@modal.asgi_app()
def vllm_app():
    """Create a FastAPI app for vLLM model serving."""
    from fastapi import FastAPI, HTTPException, Request, Depends
    from fastapi.middleware.cors import CORSMiddleware
    import time
    import uuid
    
    app = FastAPI(
        title="ContentFlow AI - vLLM Model Serving",
        description="High-performance model serving using vLLM and torch.compile",
        version="0.1.0",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Define request models
    class GenerateTextRequest(BaseModel):
        prompt: str = Field(..., description="The prompt to generate text from")
        model_name: str = Field(DEFAULT_MODEL, description="The name of the model to use")
        max_tokens: int = Field(1024, description="The maximum number of tokens to generate")
        temperature: float = Field(0.7, description="The temperature to use for sampling")
        top_p: float = Field(0.9, description="The top-p value to use for sampling")
        top_k: int = Field(50, description="The top-k value to use for sampling")
        repetition_penalty: float = Field(1.1, description="The repetition penalty to apply")
        use_torch_compile: bool = Field(True, description="Whether to use torch.compile for optimized performance")
    
    class DownloadModelRequest(BaseModel):
        model_name: str = Field(..., description="The name of the model to download")
    
    # Add request ID middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            process_time = time.time() - start_time
            return {
                "status": "error",
                "message": str(e),
                "request_id": request_id,
                "process_time": process_time,
            }
    
    # Define API routes
    @app.get("/")
    async def root():
        return {
            "message": "ContentFlow AI - vLLM Model Serving",
            "version": "0.1.0",
            "documentation": "/docs",
            "available_models": AVAILABLE_MODELS,
        }
    
    @app.get("/models")
    async def list_models():
        """List available models."""
        return {
            "models": AVAILABLE_MODELS,
            "default_model": DEFAULT_MODEL,
        }
    
    @app.post("/models/download")
    async def download_model_endpoint(request: DownloadModelRequest):
        """Download a model and save it to the model volume."""
        try:
            result = download_model.remote(request.model_name)
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": str(e),
                    "model_name": request.model_name,
                }
            )
    
    @app.post("/generate")
    async def generate_text_endpoint(request: GenerateTextRequest):
        """Generate text using vLLM with the specified model."""
        try:
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
                    "model_name": request.model_name,
                }
            )
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": "0.1.0",
            "timestamp": datetime.now().isoformat(),
        }
    
    return app


# Function to download all available models
@vllm_stub.local_entrypoint()
def download_all_models():
    """Download all available models."""
    for model_name in AVAILABLE_MODELS:
        print(f"Downloading model {model_name}...")
        result = download_model.remote(model_name)
        print(f"Result: {result}")
        print()
