"""Message bus for agent communication in ContentFlow AI.

This module defines the MessageBus class, which enables asynchronous, standardized
communication between agents. It supports multiple message types and robust error handling.
"""

from typing import Any, Dict, Optional, Callable, Awaitable
from enum import Enum
import asyncio
import uuid
import logging
from pydantic import BaseModel

logger = logging.getLogger("contentflow.communication")

class MessageType(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"
    STATUS = "status"
    ERROR = "error"

class AgentMessage(BaseModel):
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
    """
    def __init__(self):
        self._queues: Dict[str, asyncio.Queue] = {}
        self._handlers: Dict[str, Callable[[AgentMessage], Awaitable[None]]] = {}
        self._lock = asyncio.Lock()

    async def register_agent(self, agent_name: str, handler: Callable[[AgentMessage], Awaitable[None]]):
        async with self._lock:
            if agent_name not in self._queues:
                self._queues[agent_name] = asyncio.Queue()
            self._handlers[agent_name] = handler
            logger.info(f"Registered agent '{agent_name}' to message bus.")

    async def send_message(self, message: AgentMessage):
        async with self._lock:
            queue = self._queues.get(message.recipient)
            if not queue:
                logger.error(f"Recipient '{message.recipient}' not registered on message bus.")
                raise ValueError(f"Recipient '{message.recipient}' not registered.")
            await queue.put(message)
            logger.debug(f"Message {message.id} sent from '{message.sender}' to '{message.recipient}'.")

    async def listen(self, agent_name: str):
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

    @staticmethod
    def create_message(sender: str, recipient: str, type: MessageType, payload: Dict[str, Any], correlation_id: Optional[str] = None) -> AgentMessage:
        return AgentMessage(
            id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            type=type,
            payload=payload,
            correlation_id=correlation_id,
            timestamp=asyncio.get_event_loop().time()
        )
