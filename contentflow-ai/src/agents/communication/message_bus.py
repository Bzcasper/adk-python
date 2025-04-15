"""Message bus for agent communication in ContentFlow AI.

This module defines the MessageBus class, which enables asynchronous, standardized
communication between agents. It supports multiple message types and robust error handling.
"""

from typing import Any, Dict, List, Optional, Callable, Awaitable
from enum import Enum
import asyncio
import uuid
import logging
import time

logger = logging.getLogger("contentflow.communication")

class MessageType(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"
    STATUS = "status"
    ERROR = "error"
    DATA = "data"
    COMMAND = "command"

class AgentMessage:
    """Message exchanged between agents."""
    
    def __init__(
        self,
        id: str,
        sender: str,
        recipient: str,
        type: MessageType,
        payload: Dict[str, Any],
        correlation_id: Optional[str] = None,
        timestamp: Optional[float] = None,
    ):
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.type = type
        self.payload = payload
        self.correlation_id = correlation_id
        self.timestamp = timestamp or time.time()

class MessageBus:
    """
    Asynchronous message bus for agent communication.
    
    Supports sending and receiving standardized messages between agents.
    """
    def __init__(self):
        self._queues: Dict[str, asyncio.Queue] = {}
        self._handlers: Dict[str, Callable[[AgentMessage], Awaitable[None]]] = {}
        self._lock = asyncio.Lock()
        self._messages: List[AgentMessage] = []  # Store messages for history

    async def register_agent(self, agent_name: str, handler: Callable[[AgentMessage], Awaitable[None]]):
        """Register an agent with the message bus."""
        async with self._lock:
            if agent_name not in self._queues:
                self._queues[agent_name] = asyncio.Queue()
            self._handlers[agent_name] = handler
            logger.info(f"Registered agent '{agent_name}' to message bus.")
        
        # Start listening for messages
        asyncio.create_task(self.listen(agent_name))

    async def send_message(self, message: AgentMessage):
        """Send a message to an agent."""
        async with self._lock:
            queue = self._queues.get(message.recipient)
            if not queue:
                logger.error(f"Recipient '{message.recipient}' not registered on message bus.")
                raise ValueError(f"Recipient '{message.recipient}' not registered.")
            
            # Store the message in history
            self._messages.append(message)
            
            # Send the message
            await queue.put(message)
            logger.debug(f"Message {message.id} sent from '{message.sender}' to '{message.recipient}'.")

    async def listen(self, agent_name: str):
        """Listen for messages for an agent."""
        queue = self._queues.get(agent_name)
        if not queue:
            raise ValueError(f"Agent '{agent_name}' not registered.")
        
        try:
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
                queue.task_done()
        except asyncio.CancelledError:
            # Handle task cancellation gracefully
            logger.debug(f"Listener for agent '{agent_name}' cancelled.")

    def create_message(self, sender: str, recipient: str, type: MessageType, payload: Dict[str, Any], correlation_id: Optional[str] = None) -> AgentMessage:
        """Create a new message."""
        return AgentMessage(
            id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            type=type,
            payload=payload,
            correlation_id=correlation_id,
            timestamp=time.time()
        )
    
    def get_message_history(self, agent_name: Optional[str] = None):
        """Get message history, optionally filtered by agent."""
        if agent_name is None:
            return list(self._messages)  # Return a copy
        else:
            return [
                msg for msg in self._messages 
                if msg.sender == agent_name or msg.recipient == agent_name
            ]

# Create a global message bus instance
message_bus = MessageBus()