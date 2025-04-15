"""Common pytest configuration for ContentFlow AI."""

import pytest
import asyncio

@pytest.fixture
def event_loop():
    """Create a new event loop for each test."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()