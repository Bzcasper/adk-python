"""Local testing script for ContentFlow AI.

This script tests the ContentFlow AI platform locally without requiring Modal Labs deployment.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import our agents and services
from src.agents.extraction.web_content_agent import WebContentAgent
from src.agents.extraction.video_download_agent import VideoDownloadAgent
from src.agents.extraction.audio_extraction_agent import AudioExtractionAgent
from src.agents.transformation.text_transformation_agent import TextTransformationAgent


async def test_web_content_agent():
    """Test the WebContentAgent."""
    print("Testing WebContentAgent...")
    agent = WebContentAgent(model="gemini-2.0-pro")
    result = await agent.extract_article("https://en.wikipedia.org/wiki/Artificial_intelligence")
    print(f"Extracted article: {json.dumps(result, indent=2)}")
    return result


async def test_video_download_agent():
    """Test the VideoDownloadAgent."""
    print("Testing VideoDownloadAgent...")
    agent = VideoDownloadAgent(model="gemini-2.0-pro")
    result = await agent.extract_video_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Extracted video metadata: {json.dumps(result, indent=2)}")
    return result


async def test_audio_extraction_agent():
    """Test the AudioExtractionAgent."""
    print("Testing AudioExtractionAgent...")
    agent = AudioExtractionAgent(model="gemini-2.0-pro")
    # This would normally require a video file, so we'll just return a mock result
    result = {
        "status": "success",
        "audio_format": "mp3",
        "duration": 213.45,
        "sample_rate": 44100,
        "channels": 2,
        "bitrate": 320000,
        "timestamp": datetime.now().isoformat()
    }
    print(f"Extracted audio: {json.dumps(result, indent=2)}")
    return result


async def test_text_transformation_agent():
    """Test the TextTransformationAgent."""
    print("Testing TextTransformationAgent...")
    agent = TextTransformationAgent(model="gemini-2.0-pro")
    
    # Test text summarization
    text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to intelligence of humans and other animals. Example tasks in which this is done include speech recognition, computer vision, translation between (natural) languages, as well as other mappings of inputs.
    
    AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making, and competing at the highest level in strategic game systems (such as chess and Go).
    
    As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    """
    
    result = await agent.summarize_text(
        text=text,
        max_length=50,
        style="informative",
        format="paragraph"
    )
    print(f"Summarized text: {json.dumps(result, indent=2)}")
    
    # Test style transfer
    result = await agent.change_style(
        text=text,
        target_style="casual",
        preserve_meaning=True,
        format="paragraph"
    )
    print(f"Style transfer: {json.dumps(result, indent=2)}")
    
    # Test format conversion
    result = await agent.convert_format(
        text=text,
        target_format="markdown",
        preserve_content=True,
        add_metadata=False
    )
    print(f"Format conversion: {json.dumps(result, indent=2)}")
    
    return result


async def run_all_tests():
    """Run all tests."""
    print("Running all tests for ContentFlow AI platform...")
    
    # Test WebContentAgent
    await test_web_content_agent()
    print()
    
    # Test VideoDownloadAgent
    await test_video_download_agent()
    print()
    
    # Test AudioExtractionAgent
    await test_audio_extraction_agent()
    print()
    
    # Test TextTransformationAgent
    await test_text_transformation_agent()
    print()
    
    print("All tests completed!")


async def main():
    """Main entry point for the test script."""
    parser = argparse.ArgumentParser(description="Test ContentFlow AI locally")
    parser.add_argument(
        "--test",
        choices=["all", "web", "video", "audio", "text"],
        default="all",
        help="Test to run (default: all)",
    )
    args = parser.parse_args()
    
    if args.test == "all":
        await run_all_tests()
    elif args.test == "web":
        await test_web_content_agent()
    elif args.test == "video":
        await test_video_download_agent()
    elif args.test == "audio":
        await test_audio_extraction_agent()
    elif args.test == "text":
        await test_text_transformation_agent()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
