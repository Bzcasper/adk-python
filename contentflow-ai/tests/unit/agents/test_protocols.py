import os
import sys
import pytest
from dotenv import load_dotenv

load_dotenv()
pytestmark = pytest.mark.asyncio

"""Tests for agent communication protocols.

This module contains tests for the agent communication protocols in ContentFlow AI.
"""

import asyncio
from typing import Dict, Any, List
import uuid

from src.agents.communication.message_bus import MessageBus, AgentMessage
from src.agents.communication import (
    MessageType,
    AgentCommunicator,
    message_bus,
)


@pytest.fixture
async def reset_message_bus():
    """Reset the message bus between tests."""
    # Import the module to get the global message bus
    from src.agents.communication import message_bus
    
    # Store all registered agents and their handlers
    old_bus = message_bus
    
    # Create a new message bus
    from src.agents.communication.message_bus import MessageBus
    message_bus_new = MessageBus()
    
    # Replace the global message bus
    import src.agents.communication.message_bus as message_bus_module
    message_bus_module.message_bus = message_bus_new
    import src.agents.communication as comm_module
    comm_module.message_bus = message_bus_new
    
    yield message_bus_new
    
    # Restore the original message bus after the test
    message_bus_module.message_bus = old_bus
    comm_module.message_bus = old_bus


class TestAgentMessage:
    """Tests for the AgentMessage class."""

    def test_message_creation(self):
        """Test creating a message."""
        # Create a message
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender="agent1",
            recipient="agent2",
            type=MessageType.REQUEST,
            payload={"action": "extract", "url": "https://example.com"},
            correlation_id=None,
            timestamp=asyncio.get_event_loop().time()
        )
        
        # Check the message properties
        assert message.type == MessageType.REQUEST
        assert message.sender == "agent1"
        assert message.recipient == "agent2"
        assert message.payload == {"action": "extract", "url": "https://example.com"}
        assert message.correlation_id is None
        assert message.id is not None
        assert message.timestamp is not None


@pytest.mark.asyncio
class TestMessageBus:
    """Tests for the MessageBus class."""

    async def test_register_and_send(self, reset_message_bus):
        """Test registering an agent and sending a message."""
        # Create a message bus
        bus = MessageBus()
        
        # Create a list to store received messages
        received_messages = []
        
        # Create a handler function
        async def handler(message):
            received_messages.append(message)
        
        # Register an agent
        await bus.register_agent("agent1", handler)
        
        # Create a message
        message = bus.create_message(
            sender="agent2",
            recipient="agent1",
            type=MessageType.REQUEST,
            payload={"action": "extract"}
        )
        
        # Send the message
        await bus.send_message(message)
        
        # Wait for the message to be processed
        await asyncio.sleep(0.1)
        
        # Check that the message was received
        assert len(received_messages) == 1
        assert received_messages[0].sender == "agent2"
        assert received_messages[0].recipient == "agent1"
        assert received_messages[0].type == MessageType.REQUEST
        assert received_messages[0].payload == {"action": "extract"}
    
    async def test_message_history(self, reset_message_bus):
        """Test message history."""
        # Create a message bus
        bus = MessageBus()
        
        # Create a handler function
        async def handler(message):
            pass
        
        # Register agents
        await bus.register_agent("agent1", handler)
        await bus.register_agent("agent2", handler)
        
        # Create and send messages
        message1 = bus.create_message(
            sender="agent1",
            recipient="agent2",
            type=MessageType.REQUEST,
            payload={"action": "extract"}
        )
        
        message2 = bus.create_message(
            sender="agent2",
            recipient="agent1",
            type=MessageType.RESPONSE,
            payload={"status": "success"},
            correlation_id=message1.id
        )
        
        await bus.send_message(message1)
        await bus.send_message(message2)
        
        # Get message history
        history = bus.get_message_history()
        agent1_history = bus.get_message_history("agent1")
        agent2_history = bus.get_message_history("agent2")
        
        # Check history
        assert len(history) == 2
        assert len(agent1_history) == 2  # agent1 sent and received a message
        assert len(agent2_history) == 2  # agent2 sent and received a message


@pytest.mark.asyncio
class TestAgentCommunicator:
    """Tests for the AgentCommunicator class."""

    async def test_send_and_receive(self, reset_message_bus):
        """Test sending and receiving messages between agents."""
        # Create agent communicators
        agent1 = AgentCommunicator("agent1", "Agent 1")
        agent2 = AgentCommunicator("agent2", "Agent 2")
        
        # Start the agents
        await agent1.start()
        await agent2.start()
        
        # Create a list to store received messages
        received_requests = []
        received_responses = []
        
        # Create handler functions
        async def handle_request(message):
            received_requests.append(message)
            # Send a response
            await agent2.send_response(
                recipient=message.sender,
                payload={"status": "success", "data": {"title": "Example"}},
                correlation_id=message.id
            )
        
        async def handle_response(message):
            received_responses.append(message)
        
        # Register handlers
        agent2.register_handler(MessageType.REQUEST, handle_request)
        agent1.register_handler(MessageType.RESPONSE, handle_response)
        
        # Send a request
        await agent1.send_request(
            recipient="agent2",
            payload={"action": "extract", "url": "https://example.com"}
        )
        
        # Wait for the messages to be processed
        await asyncio.sleep(0.1)
        
        # Check that the messages were received
        assert len(received_requests) == 1
        assert received_requests[0].type == MessageType.REQUEST
        assert received_requests[0].sender == "agent1"
        assert received_requests[0].recipient == "agent2"
        assert received_requests[0].payload == {"action": "extract", "url": "https://example.com"}
        
        assert len(received_responses) == 1
        assert received_responses[0].type == MessageType.RESPONSE
        assert received_responses[0].sender == "agent2"
        assert received_responses[0].recipient == "agent1"
        assert received_responses[0].payload == {"status": "success", "data": {"title": "Example"}}
        assert received_responses[0].correlation_id == received_requests[0].id
    
    async def test_error_handling(self, reset_message_bus):
        """Test error handling in agent communication."""
        # Create agent communicators
        agent1 = AgentCommunicator("agent1", "Agent 1")
        agent2 = AgentCommunicator("agent2", "Agent 2")
        
        # Start the agents
        await agent1.start()
        await agent2.start()
        
        # Create a handler for agent2 that raises an exception
        async def handle_request(message):
            raise ValueError("Test error")
        
        # Register the handler
        agent2.register_handler(MessageType.REQUEST, handle_request)
        
        # Create a handler for agent1 to receive error messages
        errors = []
        
        async def handle_error(message):
            errors.append(message)
        
        # Register the handler
        agent1.register_handler(MessageType.ERROR, handle_error)
        
        # Send a request from agent1 to agent2
        request_id = await agent1.send_request(
            recipient="agent2",
            payload={"action": "extract", "url": "https://example.com"}
        )
        
        # Wait for the message to be processed
        await asyncio.sleep(0.1)
        
        # Check that agent1 received an error message
        assert len(errors) == 1
        assert errors[0].type == MessageType.ERROR
        assert errors[0].sender == "agent2"
        assert errors[0].recipient == "agent1"
        assert "error" in errors[0].payload
        assert errors[0].payload["error"] == "Test error"
        assert errors[0].correlation_id == request_id
    
    async def test_message_types(self, reset_message_bus):
        """Test different message types."""
        # Create agent communicators
        agent1 = AgentCommunicator("agent1", "Agent 1")
        agent2 = AgentCommunicator("agent2", "Agent 2")
        
        # Start the agents
        await agent1.start()
        await agent2.start()
        
        # Create handlers for different message types
        status_messages = []
        data_messages = []
        command_messages = []
        
        async def handle_status(message):
            status_messages.append(message)
        
        async def handle_data(message):
            data_messages.append(message)
        
        async def handle_command(message):
            command_messages.append(message)
        
        # Register the handlers
        agent2.register_handler(MessageType.STATUS, handle_status)
        agent2.register_handler(MessageType.DATA, handle_data)
        agent2.register_handler(MessageType.COMMAND, handle_command)
        
        # Send different types of messages
        await agent1.send_status(
            recipient="agent2",
            payload={"status": "processing", "progress": 0.5}
        )
        
        await agent1.send_data(
            recipient="agent2",
            payload={"data": [1, 2, 3]}
        )
        
        await agent1.send_command(
            recipient="agent2",
            payload={"command": "stop"}
        )
        
        # Wait for the messages to be processed
        await asyncio.sleep(0.1)
        
        # Check that agent2 received the messages
        assert len(status_messages) == 1
        assert status_messages[0].type == MessageType.STATUS
        assert status_messages[0].payload == {"status": "processing", "progress": 0.5}
        
        assert len(data_messages) == 1
        assert data_messages[0].type == MessageType.DATA
        assert data_messages[0].payload == {"data": [1, 2, 3]}
        
        assert len(command_messages) == 1
        assert command_messages[0].type == MessageType.COMMAND
        assert command_messages[0].payload == {"command": "stop"}
