"""Test script for ContentFlow AI endpoints.

This script tests the endpoints of the ContentFlow AI platform.
"""

import os
import sys
import json
import time
import argparse
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_health_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Test the health endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI API.
        
    Returns:
        The response from the health endpoint.
    """
    print("Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    response.raise_for_status()
    result = response.json()
    print(f"Health endpoint response: {json.dumps(result, indent=2)}")
    return result


def test_extraction_endpoint(base_url: str, url: str, content_type: str = "article") -> Dict[str, Any]:
    """
    Test the extraction endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI API.
        url: The URL to extract content from.
        content_type: The type of content to extract.
        
    Returns:
        The response from the extraction endpoint.
    """
    print(f"Testing extraction endpoint with URL: {url} (content_type: {content_type})...")
    response = requests.post(
        f"{base_url}/extract",
        json={
            "url": url,
            "content_type": content_type,
        },
    )
    response.raise_for_status()
    result = response.json()
    print(f"Extraction endpoint response: {json.dumps(result, indent=2)}")
    return result


def test_transformation_endpoint(
    base_url: str,
    content: Dict[str, Any],
    target_format: str,
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Test the transformation endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI API.
        content: The content to transform.
        target_format: The target format for the transformation.
        options: Optional transformation options.
        
    Returns:
        The response from the transformation endpoint.
    """
    print(f"Testing transformation endpoint with target_format: {target_format}...")
    response = requests.post(
        f"{base_url}/transform",
        json={
            "content": content,
            "target_format": target_format,
            "options": options or {},
        },
    )
    response.raise_for_status()
    result = response.json()
    print(f"Transformation endpoint response: {json.dumps(result, indent=2)}")
    return result


def test_vllm_models_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Test the vLLM models endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI vLLM API.
        
    Returns:
        The response from the models endpoint.
    """
    print("Testing vLLM models endpoint...")
    response = requests.get(f"{base_url}/models")
    response.raise_for_status()
    result = response.json()
    print(f"vLLM models endpoint response: {json.dumps(result, indent=2)}")
    return result


def test_vllm_model_info_endpoint(base_url: str, model_name: str) -> Dict[str, Any]:
    """
    Test the vLLM model info endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI vLLM API.
        model_name: The name of the model to get information about.
        
    Returns:
        The response from the model info endpoint.
    """
    print(f"Testing vLLM model info endpoint for model: {model_name}...")
    response = requests.get(f"{base_url}/models/{model_name}")
    response.raise_for_status()
    result = response.json()
    print(f"vLLM model info endpoint response: {json.dumps(result, indent=2)}")
    return result


def test_vllm_generate_endpoint(
    base_url: str,
    prompt: str,
    model_name: str = "mistral-7b",
    max_tokens: int = 512,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    """
    Test the vLLM generate endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI vLLM API.
        prompt: The prompt to generate text from.
        model_name: The name of the model to use.
        max_tokens: The maximum number of tokens to generate.
        temperature: The temperature to use for sampling.
        
    Returns:
        The response from the generate endpoint.
    """
    print(f"Testing vLLM generate endpoint with model: {model_name}...")
    response = requests.post(
        f"{base_url}/models/generate",
        json={
            "prompt": prompt,
            "model_name": model_name,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
            "use_torch_compile": True,
        },
    )
    response.raise_for_status()
    result = response.json()
    print(f"vLLM generate endpoint response: {json.dumps(result, indent=2)}")
    return result


def test_vllm_download_endpoint(base_url: str, model_name: str) -> Dict[str, Any]:
    """
    Test the vLLM download endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI vLLM API.
        model_name: The name of the model to download.
        
    Returns:
        The response from the download endpoint.
    """
    print(f"Testing vLLM download endpoint for model: {model_name}...")
    response = requests.post(f"{base_url}/models/download/{model_name}")
    response.raise_for_status()
    result = response.json()
    print(f"vLLM download endpoint response: {json.dumps(result, indent=2)}")
    return result


def test_audio_extraction_endpoint(base_url: str, url: str, audio_format: str = "mp3", quality: str = "high") -> Dict[str, Any]:
    """
    Test the audio extraction endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI API.
        url: The URL of the video to extract audio from.
        audio_format: The format of the extracted audio.
        quality: The quality of the extracted audio.
        
    Returns:
        The response from the audio extraction endpoint.
    """
    print(f"Testing audio extraction endpoint with URL: {url}...")
    try:
        response = requests.post(
            f"{base_url}/extract/audio",
            json={
                "url": url,
                "audio_format": audio_format,
                "quality": quality,
            },
        )
        response.raise_for_status()
        result = response.json()
        print(f"Audio extraction endpoint response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("="*80)
            print("WARNING: Audio extraction endpoint not found (404)")
            print("This endpoint may not be deployed yet. This is expected if you've just")
            print("added the endpoint and haven't deployed the changes to Modal.")
            print("="*80)
            result = {
                "status": "endpoint_not_found",
                "message": "The audio extraction endpoint is not available yet.",
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            print(f"Result: {json.dumps(result, indent=2)}")
            return result
        else:
            # Re-raise other HTTP errors
            raise


def test_audio_analysis_endpoint(base_url: str, url: str) -> Dict[str, Any]:
    """
    Test the audio analysis endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI API.
        url: The URL of the video to analyze audio from.
        
    Returns:
        The response from the audio analysis endpoint.
    """
    print(f"Testing audio analysis endpoint with URL: {url}...")
    try:
        response = requests.post(
            f"{base_url}/analyze/audio",
            json={
                "url": url,
            },
        )
        response.raise_for_status()
        result = response.json()
        print(f"Audio analysis endpoint response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("="*80)
            print("WARNING: Audio analysis endpoint not found (404)")
            print("This endpoint may not be deployed yet. This is expected if you've just")
            print("added the endpoint and haven't deployed the changes to Modal.")
            print("="*80)
            result = {
                "status": "endpoint_not_found",
                "message": "The audio analysis endpoint is not available yet.",
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            print(f"Result: {json.dumps(result, indent=2)}")
            return result
        else:
            # Re-raise other HTTP errors
            raise


def test_audio_transcription_endpoint(
    base_url: str, 
    url: str, 
    language: str = "en", 
    timestamps: bool = True, 
    speaker_diarization: bool = False
) -> Dict[str, Any]:
    """
    Test the audio transcription endpoint.
    
    Args:
        base_url: The base URL of the ContentFlow AI API.
        url: The URL of the video to transcribe audio from.
        language: The language of the audio content.
        timestamps: Whether to include timestamps in the transcription.
        speaker_diarization: Whether to identify different speakers.
        
    Returns:
        The response from the audio transcription endpoint.
    """
    print(f"Testing audio transcription endpoint with URL: {url}...")
    try:
        response = requests.post(
            f"{base_url}/transcribe/audio",
            json={
                "url": url,
                "language": language,
                "timestamps": timestamps,
                "speaker_diarization": speaker_diarization,
            },
        )
        response.raise_for_status()
        result = response.json()
        print(f"Audio transcription endpoint response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("="*80)
            print("WARNING: Audio transcription endpoint not found (404)")
            print("This endpoint may not be deployed yet. This is expected if you've just")
            print("added the endpoint and haven't deployed the changes to Modal.")
            print("="*80)
            result = {
                "status": "endpoint_not_found",
                "message": "The audio transcription endpoint is not available yet.",
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            print(f"Result: {json.dumps(result, indent=2)}")
            return result
        else:
            # Re-raise other HTTP errors
            raise


def run_all_tests(main_url: str, vllm_url: str) -> None:
    """
    Run all tests for the ContentFlow AI platform.
    
    Args:
        main_url: The base URL of the main ContentFlow AI API.
        vllm_url: The base URL of the ContentFlow AI vLLM API.
    """
    print(f"Running tests for ContentFlow AI platform...")
    print(f"Main API URL: {main_url}")
    print(f"vLLM API URL: {vllm_url}")
    print()
    
    # Test main API endpoints
    try:
        # Test health endpoint
        test_health_endpoint(main_url)
        print()
        
        # Test extraction endpoint
        content = test_extraction_endpoint(
            main_url,
            url="https://en.wikipedia.org/wiki/Artificial_intelligence",
            content_type="article",
        )
        print()
        
        # Test transformation endpoint
        test_transformation_endpoint(
            main_url,
            content=content,
            target_format="summary",
            options={
                "max_length": 200,
                "style": "informative",
                "format": "paragraph",
                "vllm_model": "mistral-7b",
            },
        )
        print()
        
        # Test audio extraction endpoint
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Sample video URL
        audio_result = test_audio_extraction_endpoint(
            main_url,
            url=video_url,
            audio_format="mp3",
            quality="high",
        )
        print()
        
        # Test audio analysis endpoint
        test_audio_analysis_endpoint(
            main_url,
            url=video_url,
        )
        print()
        
        # Test audio transcription endpoint
        test_audio_transcription_endpoint(
            main_url,
            url=video_url,
            language="en",
            timestamps=True,
            speaker_diarization=False,
        )
        print()
    except Exception as e:
        print(f"Error testing main API endpoints: {str(e)}")
    
    # Test vLLM API endpoints
    try:
        # Test vLLM models endpoint
        test_vllm_models_endpoint(vllm_url)
        print()
        
        # Test vLLM model info endpoint
        test_vllm_model_info_endpoint(vllm_url, model_name="mistral-7b")
        print()
        
        # Test vLLM generate endpoint
        test_vllm_generate_endpoint(
            vllm_url,
            prompt="Write a short story about a robot learning to paint.",
            model_name="mistral-7b",
            max_tokens=512,
            temperature=0.7,
        )
        print()
        
        # Test vLLM download endpoint
        test_vllm_download_endpoint(vllm_url, model_name="mistral-7b")
        print()
    except Exception as e:
        print(f"Error testing vLLM API endpoints: {str(e)}")
    
    print("All tests completed!")


def main():
    """Main entry point for the test script."""
    parser = argparse.ArgumentParser(description="Test ContentFlow AI endpoints")
    parser.add_argument(
        "--main-url",
        default="https://contentflow-ai-dev--dev.modal.run",
        help="Base URL of the main ContentFlow AI API",
    )
    parser.add_argument(
        "--vllm-url",
        default="https://contentflow-ai-vllm-dev--dev.modal.run",
        help="Base URL of the ContentFlow AI vLLM API",
    )
    parser.add_argument(
        "--test",
        choices=[
            "all", "health", "extraction", "transformation", 
            "audio-extraction", "audio-analysis", "audio-transcription",
            "vllm-models", "vllm-generate", "vllm-download"
        ],
        default="all",
        help="Test to run (default: all)",
    )
    parser.add_argument(
        "--video-url",
        default="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        help="URL of the video to use for audio tests",
    )
    args = parser.parse_args()
    
    if args.test == "all":
        run_all_tests(args.main_url, args.vllm_url)
    elif args.test == "health":
        test_health_endpoint(args.main_url)
    elif args.test == "extraction":
        test_extraction_endpoint(
            args.main_url,
            url="https://en.wikipedia.org/wiki/Artificial_intelligence",
            content_type="article",
        )
    elif args.test == "transformation":
        content = test_extraction_endpoint(
            args.main_url,
            url="https://en.wikipedia.org/wiki/Artificial_intelligence",
            content_type="article",
        )
        test_transformation_endpoint(
            args.main_url,
            content=content,
            target_format="summary",
            options={
                "max_length": 200,
                "style": "informative",
                "format": "paragraph",
                "vllm_model": "mistral-7b",
            },
        )
    elif args.test == "audio-extraction":
        test_audio_extraction_endpoint(
            args.main_url,
            url=args.video_url,
            audio_format="mp3",
            quality="high",
        )
    elif args.test == "audio-analysis":
        test_audio_analysis_endpoint(
            args.main_url,
            url=args.video_url,
        )
    elif args.test == "audio-transcription":
        test_audio_transcription_endpoint(
            args.main_url,
            url=args.video_url,
            language="en",
            timestamps=True,
            speaker_diarization=False,
        )
    elif args.test == "vllm-models":
        test_vllm_models_endpoint(args.vllm_url)
    elif args.test == "vllm-generate":
        test_vllm_generate_endpoint(
            args.vllm_url,
            prompt="Write a short story about a robot learning to paint.",
            model_name="mistral-7b",
            max_tokens=512,
            temperature=0.7,
        )
    elif args.test == "vllm-download":
        test_vllm_download_endpoint(args.vllm_url, model_name="mistral-7b")


if __name__ == "__main__":
    main()
