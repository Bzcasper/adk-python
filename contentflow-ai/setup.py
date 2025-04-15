"""Setup script for ContentFlow AI."""

from setuptools import setup, find_packages

setup(
    name="contentflow-ai",
    version="0.1.0",
    description="Intelligent content repurposing and automation platform",
    author="ContentFlow AI Team",
    author_email="info@contentflow.ai",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        # Core dependencies
        "google-adk>=0.1.0",
        "crawl4ai==0.5",
        "yt-dlp>=2023.3.4",
        "ffmpeg-python>=0.2.0",
        "pydantic>=2.0.0,<3.0.0",
        "fastapi>=0.115.0",
        "uvicorn>=0.34.0",
        "python-multipart>=0.0.9",
        
        # ML and data processing
        "transformers>=4.38.0",
        "torch>=2.2.0",
        "numpy>=1.26.0",
        "pandas>=2.2.0",
        "pillow>=10.2.0",
        
        # Modal Labs deployment
        "modal>=0.55.4",
        
        # High-performance model serving
        "vllm>=0.3.0",
        "accelerate>=0.27.0",
        "safetensors>=0.4.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.4",
            "pytest-asyncio>=0.25.0",
            "pytest-mock>=3.14.0",
        ],
    },
    python_requires=">=3.9",
)
