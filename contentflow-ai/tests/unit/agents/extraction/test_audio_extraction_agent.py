"""Tests for the AudioExtractionAgent.

This module contains tests for the AudioExtractionAgent in ContentFlow AI.
"""

import pytest
import asyncio
import os
from typing import Dict, Any
from unittest.mock import patch, MagicMock

from src.agents.extraction.audio_extraction_agent import AudioExtractionAgent


@pytest.fixture
def audio_extraction_agent():
    """Create an AudioExtractionAgent for testing."""
    return AudioExtractionAgent(model="gemini-2.0-flash")


@pytest.mark.asyncio
class TestAudioExtractionAgent:
    """Tests for the AudioExtractionAgent class."""

    async def test_extract_audio(self, audio_extraction_agent):
        """Test extracting audio from a video."""
        # Test parameters
        video_path = "/path/to/test_video.mp4"
        audio_format = "mp3"
        quality = "high"
        
        # Mock the agent's generate_content_async method
        with patch.object(
            audio_extraction_agent.agent, 
            'generate_content_async',
            return_value=MagicMock()
        ):
            # Call the extract_audio method
            result = await audio_extraction_agent.extract_audio(
                video_path=video_path,
                audio_format=audio_format,
                quality=quality
            )
            
            # Verify the result
            assert result is not None
            assert "id" in result
            assert "input_path" in result
            assert "output_path" in result
            assert "format" in result
            assert "quality" in result
            assert "metadata" in result
            assert "extraction_time" in result
            assert "agent" in result
            
            # Verify specific values
            assert result["input_path"] == video_path
            assert result["format"] == audio_format
            assert result["quality"] == quality
            assert result["agent"] == "audio_extractor"
            
            # Verify the output path is correct
            expected_output_path = "/path/to/test_video.mp3"
            assert result["output_path"] == expected_output_path
            
            # Verify metadata
            assert "duration" in result["metadata"]
            assert "sample_rate" in result["metadata"]
            assert "channels" in result["metadata"]

    async def test_enhance_audio_quality(self, audio_extraction_agent):
        """Test enhancing audio quality."""
        # Test parameters
        audio_path = "/path/to/test_audio.mp3"
        noise_reduction = True
        normalize = True
        output_format = "wav"
        
        # Mock the agent's generate_content_async method
        with patch.object(
            audio_extraction_agent.agent, 
            'generate_content_async',
            return_value=MagicMock()
        ):
            # Call the enhance_audio_quality method
            result = await audio_extraction_agent.enhance_audio_quality(
                audio_path=audio_path,
                noise_reduction=noise_reduction,
                normalize=normalize,
                output_format=output_format
            )
            
            # Verify the result
            assert result is not None
            assert "id" in result
            assert "input_path" in result
            assert "output_path" in result
            assert "format" in result
            assert "noise_reduction" in result
            assert "normalize" in result
            assert "enhancement_time" in result
            assert "agent" in result
            assert "metadata" in result
            
            # Verify specific values
            assert result["input_path"] == audio_path
            assert result["format"] == output_format
            assert result["noise_reduction"] == noise_reduction
            assert result["normalize"] == normalize
            assert result["agent"] == "audio_extractor"
            
            # Verify the output path is correct
            expected_output_path = "/path/to/test_audio_enhanced.wav"
            assert result["output_path"] == expected_output_path
            
            # Verify metadata
            assert "duration" in result["metadata"]
            assert "sample_rate" in result["metadata"]
            assert "channels" in result["metadata"]
            assert "bitrate" in result["metadata"]

    async def test_analyze_audio_content(self, audio_extraction_agent):
        """Test analyzing audio content."""
        # Test parameters
        audio_path = "/path/to/test_audio.mp3"
        
        # Mock the agent's generate_content_async method
        with patch.object(
            audio_extraction_agent.agent, 
            'generate_content_async',
            return_value=MagicMock()
        ):
            # Call the analyze_audio_content method
            result = await audio_extraction_agent.analyze_audio_content(
                audio_path=audio_path
            )
            
            # Verify the result
            assert result is not None
            assert "id" in result
            assert "audio_path" in result
            assert "analysis_time" in result
            assert "agent" in result
            assert "content_type" in result
            assert "speech_percentage" in result
            assert "music_percentage" in result
            assert "noise_percentage" in result
            assert "segments" in result
            assert "metadata" in result
            
            # Verify specific values
            assert result["audio_path"] == audio_path
            assert result["agent"] == "audio_extractor"
            
            # Verify segments
            assert len(result["segments"]) > 0
            for segment in result["segments"]:
                assert "start" in segment
                assert "end" in segment
                assert "type" in segment
                assert "confidence" in segment
            
            # Verify metadata
            assert "duration" in result["metadata"]
            assert "sample_rate" in result["metadata"]
            assert "channels" in result["metadata"]

    async def test_extract_audio_segment(self, audio_extraction_agent):
        """Test extracting an audio segment."""
        # Test parameters
        audio_path = "/path/to/test_audio.mp3"
        start_time = 60.0
        end_time = 120.0
        output_format = "wav"
        
        # Mock the agent's generate_content_async method
        with patch.object(
            audio_extraction_agent.agent, 
            'generate_content_async',
            return_value=MagicMock()
        ):
            # Call the extract_audio_segment method
            result = await audio_extraction_agent.extract_audio_segment(
                audio_path=audio_path,
                start_time=start_time,
                end_time=end_time,
                output_format=output_format
            )
            
            # Verify the result
            assert result is not None
            assert "id" in result
            assert "input_path" in result
            assert "output_path" in result
            assert "format" in result
            assert "start_time" in result
            assert "end_time" in result
            assert "duration" in result
            assert "extraction_time" in result
            assert "agent" in result
            assert "metadata" in result
            
            # Verify specific values
            assert result["input_path"] == audio_path
            assert result["format"] == output_format
            assert result["start_time"] == start_time
            assert result["end_time"] == end_time
            assert result["duration"] == end_time - start_time
            assert result["agent"] == "audio_extractor"
            
            # Verify the output path is correct
            expected_output_path = "/path/to/test_audio_segment_60-120.wav"
            assert result["output_path"] == expected_output_path
            
            # Verify metadata
            assert "duration" in result["metadata"]
            assert "sample_rate" in result["metadata"]
            assert "channels" in result["metadata"]
            assert "bitrate" in result["metadata"]
