"""Agent communicator for ContentFlow AI.

This module defines the AgentCommunicator class, which provides a high-level
interface for agent communication using the message bus.
"""

from typing import Dict, Any, Optional, Callable, Awaitable
import asyncio
import logging

from .message_bus import MessageBus, AgentMessage, MessageType, message_bus

logger = logging.getLogger("contentflow.communication")

class AgentCommunicator:
    """Interface for agent communication."""
    
    def __init__(self, agent_id: str, agent_name: str, message_bus=message_bus):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.message_bus = message_bus
        self._handlers: Dict[MessageType, Callable[[AgentMessage], Awaitable[None]]] = {}
        self._started = False
    
    async def start(self):
        """Start the agent communicator."""
        if not self._started:
            # Register with the message bus
            await self.message_bus.register_agent(self.agent_id, self._handle_message)
            self._started = True
            logger.info(f"Agent communicator for '{self.agent_name}' ({self.agent_id}) started.")
    
    async def _handle_message(self, message: AgentMessage):
        """Handle an incoming message."""
        logger.debug(f"Agent {self.agent_id} received message: {message.id} ({message.type})")
        
        # Call the appropriate handler for the message type
        handler = self._handlers.get(message.type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Error handling message {message.id}: {str(e)}")
                
                # Send an error response if appropriate
                if message.type == MessageType.REQUEST:
                    await self.send_error(
                        recipient=message.sender,
                        payload={"error": str(e)},
                        correlation_id=message.id
                    )
        else:
            logger.warning(f"No handler registered for message type {message.type}")
    
    def register_handler(self, message_type: MessageType, handler: Callable[[AgentMessage], Awaitable[None]]):
        """Register a handler for a message type."""
        self._handlers[message_type] = handler
        logger.debug(f"Agent {self.agent_id} registered handler for {message_type}")
    
    async def send_message(self, type: MessageType, recipient: str, payload: Dict[str, Any], correlation_id: Optional[str] = None):
        """Send a message."""
        message = self.message_bus.create_message(
            sender=self.agent_id,
            recipient=recipient,
            type=type,
            payload=payload,
            correlation_id=correlation_id
        )
        
        await self.message_bus.send_message(message)
        return message.id
    
    async def send_request(self, recipient: str, payload: Dict[str, Any]):
        """Send a request message."""
        return await self.send_message(
            type=MessageType.REQUEST,
            recipient=recipient,
            payload=payload
        )
    
    async def send_response(self, recipient: str, payload: Dict[str, Any], correlation_id: Optional[str] = None):
        """Send a response message."""
        return await self.send_message(
            type=MessageType.RESPONSE,
            recipient=recipient,
            payload=payload,
            correlation_id=correlation_id
        )
    
    async def send_error(self, recipient: str, payload: Dict[str, Any], correlation_id: Optional[str] = None):
        """Send an error message."""
        return await self.send_message(
            type=MessageType.ERROR,
            recipient=recipient,
            payload=payload,
            correlation_id=correlation_id
        )
    
    async def send_status(self, recipient: str, payload: Dict[str, Any]):
        """Send a status message."""
        return await self.send_message(
            type=MessageType.STATUS,
            recipient=recipient,
            payload=payload
        )
    
    async def send_data(self, recipient: str, payload: Dict[str, Any]):
        """Send a data message."""
        return await self.send_message(
            type=MessageType.DATA,
            recipient=recipient,
            payload=payload
        )
    
    async def send_command(self, recipient: str, payload: Dict[str, Any]):
        """Send a command message."""
        return await self.send_message(
            type=MessageType.COMMAND,
            recipient=recipient,
            payload=payload
        )