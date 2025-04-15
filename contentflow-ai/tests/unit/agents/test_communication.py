"""Tests for agent communication protocols.

This module contains tests for the agent communication protocols in ContentFlow AI.
"""

import pytest
import asyncio
from typing import Dict, Any, List
import uuid

# Import from the module file, not the directory
from src.agents.communication import (
    MessageType,
    Message,
    MessageBus,
    AgentCommunicator,
    message_bus,
)


@pytest.fixture
def reset_message_bus():
    """Reset the message bus between tests."""
    # Create a new message bus instance
    global message_bus
    message_bus = MessageBus()
    yield
    # Clean up after the test
    message_bus = MessageBus()


class TestMessage:
    """Tests for the Message class."""

    def test_message_creation(self):
        """Test creating a message."""
        # Create a message
        message = Message(
            message_type=MessageType.REQUEST,
            sender="agent1",
            recipient="agent2",
            content={"action": "extract", "url": "https://example.com"},
            metadata={"priority": "high"},
        )
        
        # Check the message properties
        assert message.message_type == MessageType.REQUEST
        assert message.sender == "agent1"
        assert message.recipient == "agent2"
        assert message.content == {"action": "extract", "url": "https://example.com"}
        assert message.metadata == {"priority": "high"}
        assert message.message_id is not None
        assert message.in_reply_to is None
        assert message.timestamp is not None
    
    def test_message_to_dict(self):
        """Test converting a message to a dictionary."""
        # Create a message
        message = Message(
            message_type=MessageType.RESPONSE,
            sender="agent2",
            recipient="agent1",
            content={"status": "success", "data": {"title": "Example"}},
            metadata={"processing_time": 1.5},
            message_id="test-id",
            in_reply_to="request-id",
        )
        
        # Convert to dictionary
        message_dict = message.to_dict()
        
        # Check the dictionary
        assert message_dict["message_type"] == MessageType.RESPONSE
        assert message_dict["sender"] == "agent2"
        assert message_dict["recipient"] == "agent1"
        assert message_dict["content"] == {"status": "success", "data": {"title": "Example"}}
        assert message_dict["metadata"] == {"processing_time": 1.5}
        assert message_dict["message_id"] == "test-id"
        assert message_dict["in_reply_to"] == "request-id"
        assert message_dict["timestamp"] is not None
    
    def test_message_from_dict(self):
        """Test creating a message from a dictionary."""
        # Create a dictionary
        message_dict = {
            "message_type": MessageType.DATA,
            "sender": "agent3",
            "recipient": "agent4",
            "content": {"data": [1, 2, 3]},
            "metadata": {"source": "database"},
            "message_id": "data-id",
            "in_reply_to": None,
            "timestamp": "2025-04-15T12:00:00",
        }
        
        # Create a message from the dictionary
        message = Message.from_dict(message_dict)
        
        # Check the message
        assert message.message_type == MessageType.DATA
        assert message.sender == "agent3"
        assert message.recipient == "agent4"
        assert message.content == {"data": [1, 2, 3]}
        assert message.metadata == {"source": "database"}
        assert message.message_id == "data-id"
        assert message.in_reply_to is None


@pytest.mark.asyncio
class TestMessageBus:
    """Tests for the MessageBus class."""

    async def test_publish_and_subscribe(self, reset_message_bus):
        """Test publishing and subscribing to messages."""
        # Create a message bus
        bus = MessageBus()
        
        # Create a message
        message = Message(
            message_type=MessageType.REQUEST,
            sender="agent1",
            recipient="agent2",
            content={"action": "extract"},
        )
        
        # Create a callback function
        received_messages = []
        
        async def callback(msg):
            received_messages.append(msg)
        
        # Subscribe to messages
        bus.subscribe("agent2", callback)
        
        # Publish a message
        await bus.publish(message)
        
        # Check that the message was received
        assert len(received_messages) == 1
        assert received_messages[0].message_id == message.message_id
        assert received_messages[0].message_type == MessageType.REQUEST
        assert received_messages[0].sender == "agent1"
        assert received_messages[0].recipient == "agent2"
        assert received_messages[0].content == {"action": "extract"}
    
    async def test_message_history(self, reset_message_bus):
        """Test message history."""
        # Create a message bus
        bus = MessageBus()
        
        # Create messages
        message1 = Message(
            message_type=MessageType.REQUEST,
            sender="agent1",
            recipient="agent2",
            content={"action": "extract"},
        )
        
        message2 = Message(
            message_type=MessageType.RESPONSE,
            sender="agent2",
            recipient="agent1",
            content={"status": "success"},
            in_reply_to=message1.message_id,
        )
        
        # Publish messages
        await bus.publish(message1)
        await bus.publish(message2)
        
        # Check the message history
        history = bus.get_message_history()
        assert len(history) == 2
        assert history[0].message_id == message1.message_id
        assert history[1].message_id == message2.message_id
        
        # Check the message history for a specific agent
        agent1_history = bus.get_message_history("agent1")
        assert len(agent1_history) == 2
        
        agent2_history = bus.get_message_history("agent2")
        assert len(agent2_history) == 2
        
        agent3_history = bus.get_message_history("agent3")
        assert len(agent3_history) == 0
    
    async def test_unsubscribe(self, reset_message_bus):
        """Test unsubscribing from messages."""
        # Create a message bus
        bus = MessageBus()
        
        # Create a message
        message = Message(
            message_type=MessageType.REQUEST,
            sender="agent1",
            recipient="agent2",
            content={"action": "extract"},
        )
        
        # Create callback functions
        received_messages1 = []
        received_messages2 = []
        
        async def callback1(msg):
            received_messages1.append(msg)
        
        async def callback2(msg):
            received_messages2.append(msg)
        
        # Subscribe to messages
        bus.subscribe("agent2", callback1)
        bus.subscribe("agent2", callback2)
        
        # Publish a message
        await bus.publish(message)
        
        # Check that both callbacks received the message
        assert len(received_messages1) == 1
        assert len(received_messages2) == 1
        
        # Unsubscribe one callback
        bus.unsubscribe("agent2", callback1)
        
        # Publish another message
        await bus.publish(message)
        
        # Check that only the second callback received the message
        assert len(received_messages1) == 1
        assert len(received_messages2) == 2
        
        # Unsubscribe all callbacks
        bus.unsubscribe("agent2")
        
        # Publish another message
        await bus.publish(message)
        
        # Check that no callbacks received the message
        assert len(received_messages1) == 1
        assert len(received_messages2) == 2


@pytest.mark.asyncio
class TestAgentCommunicator:
    """Tests for the AgentCommunicator class."""

    async def test_send_and_receive_message(self, reset_message_bus):
        """Test sending and receiving messages between agents."""
        # Create agent communicators
        agent1 = AgentCommunicator(agent_id="agent1", agent_name="Agent 1")
        agent2 = AgentCommunicator(agent_id="agent2", agent_name="Agent 2")
        
        # Create a handler for agent2
        received_messages = []
        
        async def handle_request(message):
            received_messages.append(message)
            
            # Send a response
            await agent2.send_response(
                recipient=message.sender,
                content={"status": "success", "data": {"title": "Example"}},
                in_reply_to=message.message_id,
            )
        
        # Register the handler
        agent2.register_handler(MessageType.REQUEST, handle_request)
        
        # Create a handler for agent1
        responses = []
        
        async def handle_response(message):
            responses.append(message)
        
        # Register the handler
        agent1.register_handler(MessageType.RESPONSE, handle_response)
        
        # Send a request from agent1 to agent2
        await agent1.send_request(
            recipient="agent2",
            content={"action": "extract", "url": "https://example.com"},
        )
        
        # Wait for the message to be processed
        await asyncio.sleep(0.1)
        
        # Check that agent2 received the request
        assert len(received_messages) == 1
        assert received_messages[0].message_type == MessageType.REQUEST
        assert received_messages[0].sender == "agent1"
        assert received_messages[0].recipient == "agent2"
        assert received_messages[0].content == {"action": "extract", "url": "https://example.com"}
        
        # Check that agent1 received the response
        assert len(responses) == 1
        assert responses[0].message_type == MessageType.RESPONSE
        assert responses[0].sender == "agent2"
        assert responses[0].recipient == "agent1"
        assert responses[0].content == {"status": "success", "data": {"title": "Example"}}
        assert responses[0].in_reply_to == received_messages[0].message_id
    
    async def test_error_handling(self, reset_message_bus):
        """Test error handling in agent communication."""
        # Create agent communicators
        agent1 = AgentCommunicator(agent_id="agent1", agent_name="Agent 1")
        agent2 = AgentCommunicator(agent_id="agent2", agent_name="Agent 2")
        
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
            content={"action": "extract", "url": "https://example.com"},
        )
        
        # Wait for the message to be processed
        await asyncio.sleep(0.1)
        
        # Check that agent1 received an error message
        assert len(errors) == 1
        assert errors[0].message_type == MessageType.ERROR
        assert errors[0].sender == "agent2"
        assert errors[0].recipient == "agent1"
        assert "error" in errors[0].content
        assert errors[0].content["error"] == "Test error"
        assert errors[0].in_reply_to == request_id
    
    async def test_message_types(self, reset_message_bus):
        """Test different message types."""
        # Create agent communicators
        agent1 = AgentCommunicator(agent_id="agent1", agent_name="Agent 1")
        agent2 = AgentCommunicator(agent_id="agent2", agent_name="Agent 2")
        
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
            content={"status": "processing", "progress": 0.5},
        )
        
        await agent1.send_data(
            recipient="agent2",
            content={"data": [1, 2, 3]},
        )
        
        await agent1.send_command(
            recipient="agent2",
            content={"command": "stop"},
        )
        
        # Wait for the messages to be processed
        await asyncio.sleep(0.1)
        
        # Check that agent2 received the messages
        assert len(status_messages) == 1
        assert status_messages[0].message_type == MessageType.STATUS
        assert status_messages[0].content == {"status": "processing", "progress": 0.5}
        
        assert len(data_messages) == 1
        assert data_messages[0].message_type == MessageType.DATA
        assert data_messages[0].content == {"data": [1, 2, 3]}
        
        assert len(command_messages) == 1
        assert command_messages[0].message_type == MessageType.COMMAND
        assert command_messages[0].content == {"command": "stop"}
