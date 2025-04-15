"""Agent communication protocols for ContentFlow AI.

This module defines the communication protocols between agents in the ContentFlow AI
platform, enabling seamless interaction and data exchange between extraction,
transformation, and distribution agents.
"""

from typing import Dict, List, Optional, Any, Union, Callable, Awaitable
from enum import Enum
import asyncio
import uuid
from datetime import datetime
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """Types of messages that can be exchanged between agents."""
    
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    STATUS = "status"
    DATA = "data"
    COMMAND = "command"


class Message:
    """Message exchanged between agents.
    
    This class represents a message that can be exchanged between agents in the
    ContentFlow AI platform. Messages have a type, sender, recipient, content,
    and optional metadata.
    """
    
    def __init__(
        self,
        message_type: MessageType,
        sender: str,
        recipient: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
        message_id: Optional[str] = None,
        in_reply_to: Optional[str] = None,
    ):
        """
        Initialize a Message.
        
        Args:
            message_type: The type of message.
            sender: The ID of the agent sending the message.
            recipient: The ID of the agent receiving the message.
            content: The content of the message.
            metadata: Optional metadata about the message.
            message_id: Optional ID for the message. If not provided, a UUID will be generated.
            in_reply_to: Optional ID of the message this message is replying to.
        """
        self.message_type = message_type
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.metadata = metadata or {}
        self.message_id = message_id or str(uuid.uuid4())
        self.in_reply_to = in_reply_to
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary.
        
        Returns:
            A dictionary representation of the message.
        """
        return {
            "message_id": self.message_id,
            "message_type": self.message_type,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "metadata": self.metadata,
            "in_reply_to": self.in_reply_to,
            "timestamp": self.timestamp,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """
        Create a Message from a dictionary.
        
        Args:
            data: A dictionary representation of a message.
            
        Returns:
            A Message object.
        """
        return cls(
            message_type=data["message_type"],
            sender=data["sender"],
            recipient=data["recipient"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            message_id=data.get("message_id"),
            in_reply_to=data.get("in_reply_to"),
        )
    
    def __str__(self) -> str:
        """
        Get a string representation of the message.
        
        Returns:
            A string representation of the message.
        """
        return f"Message({self.message_type}, {self.sender} -> {self.recipient}, {self.message_id})"


class MessageBus:
    """Message bus for agent communication.
    
    This class provides a message bus for agents to communicate with each other.
    It handles message routing, delivery, and processing.
    """
    
    def __init__(self):
        """Initialize the MessageBus."""
        self.subscribers: Dict[str, List[Callable[[Message], Awaitable[None]]]] = {}
        self.message_history: List[Message] = []
        self.max_history_size = 1000  # Maximum number of messages to keep in history
    
    async def publish(self, message: Message) -> None:
        """
        Publish a message to the message bus.
        
        Args:
            message: The message to publish.
        """
        # Log the message
        logger.debug(f"Publishing message: {message}")
        
        # Add the message to the history
        self.message_history.append(message)
        
        # Trim the history if it's too large
        if len(self.message_history) > self.max_history_size:
            self.message_history = self.message_history[-self.max_history_size:]
        
        # Deliver the message to subscribers
        if message.recipient in self.subscribers:
            for callback in self.subscribers[message.recipient]:
                try:
                    await callback(message)
                except Exception as e:
                    logger.error(f"Error delivering message to {message.recipient}: {str(e)}")
    
    def subscribe(self, agent_id: str, callback: Callable[[Message], Awaitable[None]]) -> None:
        """
        Subscribe to messages for a specific agent.
        
        Args:
            agent_id: The ID of the agent to subscribe for.
            callback: The callback function to call when a message is received.
        """
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        
        self.subscribers[agent_id].append(callback)
        logger.debug(f"Agent {agent_id} subscribed to message bus")
    
    def unsubscribe(self, agent_id: str, callback: Optional[Callable[[Message], Awaitable[None]]] = None) -> None:
        """
        Unsubscribe from messages for a specific agent.
        
        Args:
            agent_id: The ID of the agent to unsubscribe.
            callback: The callback function to unsubscribe. If None, all callbacks for the agent will be unsubscribed.
        """
        if agent_id not in self.subscribers:
            return
        
        if callback is None:
            self.subscribers[agent_id] = []
            logger.debug(f"Agent {agent_id} unsubscribed from all messages")
        else:
            self.subscribers[agent_id] = [cb for cb in self.subscribers[agent_id] if cb != callback]
            logger.debug(f"Agent {agent_id} unsubscribed from specific callback")
    
    def get_message_history(self, agent_id: Optional[str] = None) -> List[Message]:
        """
        Get the message history for a specific agent or all agents.
        
        Args:
            agent_id: The ID of the agent to get history for. If None, all messages will be returned.
            
        Returns:
            A list of messages.
        """
        if agent_id is None:
            return self.message_history
        
        return [
            message for message in self.message_history
            if message.sender == agent_id or message.recipient == agent_id
        ]


# Create a global message bus instance
message_bus = MessageBus()


class AgentCommunicator:
    """Agent communicator for ContentFlow AI agents.
    
    This class provides communication capabilities for agents in the ContentFlow AI
    platform. It handles sending and receiving messages, as well as processing
    incoming messages.
    """
    
    def __init__(self, agent_id: str, agent_name: str):
        """
        Initialize an AgentCommunicator.
        
        Args:
            agent_id: The ID of the agent.
            agent_name: The name of the agent.
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.message_handlers: Dict[MessageType, Callable[[Message], Awaitable[None]]] = {}
        
        # Subscribe to messages for this agent
        message_bus.subscribe(agent_id, self._process_message)
    
    async def _process_message(self, message: Message) -> None:
        """
        Process an incoming message.
        
        Args:
            message: The message to process.
        """
        # Log the message
        logger.debug(f"Agent {self.agent_id} received message: {message}")
        
        # Process the message based on its type
        if message.message_type in self.message_handlers:
            try:
                await self.message_handlers[message.message_type](message)
            except Exception as e:
                logger.error(f"Error processing message {message.message_id}: {str(e)}")
                
                # Send an error response
                await self.send_error(
                    recipient=message.sender,
                    content={"error": str(e)},
                    in_reply_to=message.message_id,
                )
    
    def register_handler(
        self, 
        message_type: MessageType, 
        handler: Callable[[Message], Awaitable[None]]
    ) -> None:
        """
        Register a handler for a specific message type.
        
        Args:
            message_type: The type of message to handle.
            handler: The handler function to call when a message of this type is received.
        """
        self.message_handlers[message_type] = handler
        logger.debug(f"Agent {self.agent_id} registered handler for {message_type}")
    
    async def send_message(
        self,
        message_type: MessageType,
        recipient: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
        in_reply_to: Optional[str] = None,
    ) -> str:
        """
        Send a message to another agent.
        
        Args:
            message_type: The type of message to send.
            recipient: The ID of the agent to send the message to.
            content: The content of the message.
            metadata: Optional metadata about the message.
            in_reply_to: Optional ID of the message this message is replying to.
            
        Returns:
            The ID of the sent message.
        """
        message = Message(
            message_type=message_type,
            sender=self.agent_id,
            recipient=recipient,
            content=content,
            metadata=metadata,
            in_reply_to=in_reply_to,
        )
        
        await message_bus.publish(message)
        return message.message_id
    
    async def send_request(
        self,
        recipient: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Send a request message to another agent.
        
        Args:
            recipient: The ID of the agent to send the request to.
            content: The content of the request.
            metadata: Optional metadata about the request.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            message_type=MessageType.REQUEST,
            recipient=recipient,
            content=content,
            metadata=metadata,
        )
    
    async def send_response(
        self,
        recipient: str,
        content: Any,
        in_reply_to: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Send a response message to another agent.
        
        Args:
            recipient: The ID of the agent to send the response to.
            content: The content of the response.
            in_reply_to: The ID of the message this response is replying to.
            metadata: Optional metadata about the response.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            message_type=MessageType.RESPONSE,
            recipient=recipient,
            content=content,
            metadata=metadata,
            in_reply_to=in_reply_to,
        )
    
    async def send_error(
        self,
        recipient: str,
        content: Any,
        in_reply_to: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Send an error message to another agent.
        
        Args:
            recipient: The ID of the agent to send the error to.
            content: The content of the error.
            in_reply_to: Optional ID of the message this error is replying to.
            metadata: Optional metadata about the error.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            message_type=MessageType.ERROR,
            recipient=recipient,
            content=content,
            metadata=metadata,
            in_reply_to=in_reply_to,
        )
    
    async def send_status(
        self,
        recipient: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Send a status message to another agent.
        
        Args:
            recipient: The ID of the agent to send the status to.
            content: The content of the status.
            metadata: Optional metadata about the status.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            message_type=MessageType.STATUS,
            recipient=recipient,
            content=content,
            metadata=metadata,
        )
    
    async def send_data(
        self,
        recipient: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Send a data message to another agent.
        
        Args:
            recipient: The ID of the agent to send the data to.
            content: The content of the data.
            metadata: Optional metadata about the data.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            message_type=MessageType.DATA,
            recipient=recipient,
            content=content,
            metadata=metadata,
        )
    
    async def send_command(
        self,
        recipient: str,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Send a command message to another agent.
        
        Args:
            recipient: The ID of the agent to send the command to.
            content: The content of the command.
            metadata: Optional metadata about the command.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            message_type=MessageType.COMMAND,
            recipient=recipient,
            content=content,
            metadata=metadata,
        )
    
    def cleanup(self) -> None:
        """Clean up resources used by the communicator."""
        message_bus.unsubscribe(self.agent_id)
        logger.debug(f"Agent {self.agent_id} cleaned up")
