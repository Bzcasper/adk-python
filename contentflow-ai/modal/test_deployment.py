"""Test script for ContentFlow AI Modal Labs deployment.

This script tests the ContentFlow AI Modal Labs deployment by running a simple
extraction task and verifying that it works correctly.
"""

import os
import sys
import time
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the deployment configuration
from modal.deployment import stub, extract_content


def test_extraction():
    """Test the extraction functionality."""
    print("Testing ContentFlow AI extraction functionality...")
    
    # Test URLs for different content types
    test_urls = {
        "article": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    }
    
    # Test each content type
    for content_type, url in test_urls.items():
        print(f"\nTesting {content_type} extraction from {url}...")
        start_time = time.time()
        
        # Run the extraction function
        with stub.run():
            result = extract_content.remote(url, content_type)
            
        # Print the result
        print(f"Extraction completed in {time.time() - start_time:.2f} seconds")
        print(f"Result: {result}")
        
        # Verify the result
        assert "url" in result, "URL not found in result"
        assert result["url"] == url, "URL in result doesn't match input URL"
        
        if content_type == "article":
            assert "title" in result, "Title not found in result"
            assert "content" in result, "Content not found in result"
            assert "metadata" in result, "Metadata not found in result"
        elif content_type == "video":
            assert "title" in result, "Title not found in result"
            assert "duration" in result, "Duration not found in result"
            assert "metadata" in result, "Metadata not found in result"
        
        print(f"{content_type.capitalize()} extraction test passed!")
    
    print("\nAll extraction tests passed!")


def test_api():
    """Test the API functionality."""
    print("\nTesting ContentFlow AI API functionality...")
    
    # Run the API function to get the URL
    with stub.run():
        app_url = stub.api.remote()
        
    print(f"API deployed at: {app_url}")
    print("API test passed!")


def main():
    """Main entry point for the test script."""
    print(f"Starting ContentFlow AI deployment tests at {datetime.now().isoformat()}")
    
    # Test extraction functionality
    test_extraction()
    
    # Test API functionality
    test_api()
    
    print(f"\nAll tests passed at {datetime.now().isoformat()}!")
    print("ContentFlow AI Modal Labs deployment is working correctly.")


if __name__ == "__main__":
    main()
