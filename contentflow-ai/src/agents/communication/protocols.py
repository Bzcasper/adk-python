"""Agent communication protocol implementation for ContentFlow AI.

This module implements the communication protocols for ContentFlow AI agents,
providing standardized message types, message bus, and agent communicator.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from enum import Enum
import asyncio
import uuid
import logging
from pydantic import BaseModel

logger = logging.getLogger("contentflow.communication")

class MessageType(str, Enum):
    """Types of messages that can be exchanged between agents."""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    STATUS = "status"
    DATA = "data"
    COMMAND = "command"

class AgentMessage(BaseModel):
    """Message exchanged between agents."""
    id: str
    sender: str
    recipient: str
    type: MessageType
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    timestamp: float

class MessageBus:
    """
    Asynchronous message bus for agent communication.
    
    Supports sending and receiving standardized messages between agents.
    Provides robust error handling and message correlation.
    """
    def __init__(self):
        """Initialize the message bus."""
        self._queues: Dict[str, asyncio.Queue] = {}
        self._handlers: Dict[str, Callable[[AgentMessage], Awaitable[None]]] = {}
        self._lock = asyncio.Lock()
        self._message_history: List[AgentMessage] = []
        self._max_history_size = 1000

    async def register_agent(self, agent_name: str, handler: Callable[[AgentMessage], Awaitable[None]]):
        """
        Register an agent with the message bus.
        
        Args:
            agent_name: The name of the agent.
            handler: The handler function to call when a message is received.
        """
        async with self._lock:
            if agent_name not in self._queues:
                self._queues[agent_name] = asyncio.Queue()
            self._handlers[agent_name] = handler
            logger.info(f"Registered agent '{agent_name}' to message bus.")

    async def send_message(self, message: AgentMessage):
        """
        Send a message to an agent.
        
        Args:
            message: The message to send.
            
        Raises:
            ValueError: If the recipient is not registered.
        """
        async with self._lock:
            queue = self._queues.get(message.recipient)
            if not queue:
                logger.error(f"Recipient '{message.recipient}' not registered on message bus.")
                raise ValueError(f"Recipient '{message.recipient}' not registered.")
            await queue.put(message)
            # Add to history
            self._message_history.append(message)
            if len(self._message_history) > self._max_history_size:
                self._message_history.pop(0)
            logger.debug(f"Message {message.id} sent from '{message.sender}' to '{message.recipient}'.")

    async def listen(self, agent_name: str):
        """
        Listen for messages for an agent.
        
        Args:
            agent_name: The name of the agent to listen for.
            
        Raises:
            ValueError: If the agent is not registered.
        """
        queue = self._queues.get(agent_name)
        if not queue:
            raise ValueError(f"Agent '{agent_name}' not registered.")
        while True:
            message = await queue.get()
            handler = self._handlers.get(agent_name)
            if handler:
                try:
                    await handler(message)
                except Exception as e:
                    logger.error(f"Error handling message {message.id}: {str(e)}")
            else:
                logger.warning(f"No handler registered for agent '{agent_name}'.")

    def get_message_history(self, agent_id: Optional[str] = None) -> List[AgentMessage]:
        """
        Get the message history for a specific agent or all agents.
        
        Args:
            agent_id: The ID of the agent to get history for. If None, all messages will be returned.
            
        Returns:
            A list of messages.
        """
        if agent_id is None:
            return self._message_history
        
        return [
            message for message in self._message_history
            if message.sender == agent_id or message.recipient == agent_id
        ]

    @staticmethod
    def create_message(sender: str, recipient: str, type: MessageType, payload: Dict[str, Any], correlation_id: Optional[str] = None) -> AgentMessage:
        """
        Create a new message.
        
        Args:
            sender: The sender of the message.
            recipient: The recipient of the message.
            type: The type of message.
            payload: The payload of the message.
            correlation_id: Optional correlation ID for request/response correlation.
            
        Returns:
            A new AgentMessage.
        """
        return AgentMessage(
            id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            type=type,
            payload=payload,
            correlation_id=correlation_id,
            timestamp=asyncio.get_event_loop().time()
        )

class AgentCommunicator:
    """
    Agent communicator for ContentFlow AI agents.
    
    Provides a high-level interface for agents to communicate with each other.
    Supports all message types and robust error handling.
    """
    
    def __init__(self, agent_id: str, agent_name: str):
        """
        Initialize an agent communicator.
        
        Args:
            agent_id: The ID of the agent.
            agent_name: The name of the agent.
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.message_bus = MessageBus()
        self.handlers: Dict[MessageType, Callable[[AgentMessage], Awaitable[None]]] = {}
        
    async def start(self):
        """Start the agent communicator."""
        await self.message_bus.register_agent(self.agent_id, self._handle_message)
        asyncio.create_task(self.message_bus.listen(self.agent_id))
        logger.info(f"Agent communicator for {self.agent_name} ({self.agent_id}) started.")
        
    async def _handle_message(self, message: AgentMessage):
        """
        Handle an incoming message.
        
        Args:
            message: The message to handle.
        """
        handler = self.handlers.get(message.type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Error handling message {message.id}: {str(e)}")
                if message.type == MessageType.REQUEST:
                    # Send error response for request messages
                    await self.send_error(
                        recipient=message.sender,
                        payload={"error": str(e)},
                        correlation_id=message.id
                    )
        else:
            logger.warning(f"No handler registered for message type {message.type}.")
            
    def register_handler(self, message_type: MessageType, handler: Callable[[AgentMessage], Awaitable[None]]):
        """
        Register a handler for a specific message type.
        
        Args:
            message_type: The type of message to handle.
            handler: The handler function to call when a message of this type is received.
        """
        self.handlers[message_type] = handler
        logger.debug(f"Registered handler for message type {message_type}.")
        
    async def send_message(self, recipient: str, type: MessageType, payload: Dict[str, Any], correlation_id: Optional[str] = None) -> str:
        """
        Send a message to another agent.
        
        Args:
            recipient: The ID of the agent to send the message to.
            type: The type of message to send.
            payload: The payload of the message.
            correlation_id: Optional correlation ID for request/response correlation.
            
        Returns:
            The ID of the sent message.
        """
        message = self.message_bus.create_message(
            sender=self.agent_id,
            recipient=recipient,
            type=type,
            payload=payload,
            correlation_id=correlation_id
        )
        await self.message_bus.send_message(message)
        return message.id
        
    async def send_request(self, recipient: str, payload: Dict[str, Any]) -> str:
        """
        Send a request message to another agent.
        
        Args:
            recipient: The ID of the agent to send the request to.
            payload: The payload of the request.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            recipient=recipient,
            type=MessageType.REQUEST,
            payload=payload
        )
        
    async def send_response(self, recipient: str, payload: Dict[str, Any], correlation_id: str) -> str:
        """
        Send a response message to another agent.
        
        Args:
            recipient: The ID of the agent to send the response to.
            payload: The payload of the response.
            correlation_id: The ID of the request message this response is for.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            recipient=recipient,
            type=MessageType.RESPONSE,
            payload=payload,
            correlation_id=correlation_id
        )
        
    async def send_error(self, recipient: str, payload: Dict[str, Any], correlation_id: Optional[str] = None) -> str:
        """
        Send an error message to another agent.
        
        Args:
            recipient: The ID of the agent to send the error to.
            payload: The payload of the error.
            correlation_id: Optional correlation ID for the request message this error is for.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            recipient=recipient,
            type=MessageType.ERROR,
            payload=payload,
            correlation_id=correlation_id
        )
        
    async def send_status(self, recipient: str, payload: Dict[str, Any]) -> str:
        """
        Send a status message to another agent.
        
        Args:
            recipient: The ID of the agent to send the status to.
            payload: The payload of the status.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            recipient=recipient,
            type=MessageType.STATUS,
            payload=payload
        )
        
    async def send_data(self, recipient: str, payload: Dict[str, Any]) -> str:
        """
        Send a data message to another agent.
        
        Args:
            recipient: The ID of the agent to send the data to.
            payload: The payload of the data.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            recipient=recipient,
            type=MessageType.DATA,
            payload=payload
        )
        
    async def send_command(self, recipient: str, payload: Dict[str, Any]) -> str:
        """
        Send a command message to another agent.
        
        Args:
            recipient: The ID of the agent to send the command to.
            payload: The payload of the command.
            
        Returns:
            The ID of the sent message.
        """
        return await self.send_message(
            recipient=recipient,
            type=MessageType.COMMAND,
            payload=payload
        )
