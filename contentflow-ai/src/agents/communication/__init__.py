"""Agent communication package for ContentFlow AI.

This package provides the communication infrastructure for agents in ContentFlow AI,
including message types, message bus, and agent communicator.
"""

"""Agent communication package for ContentFlow AI.

This package provides the communication infrastructure for agents in ContentFlow AI,
including message types, message bus, and agent communicator.
"""

# Import from the protocols module to make these available at the package level
from .protocols import (
    MessageType, AgentMessage, MessageBus, AgentCommunicator
)

# Create a global message bus instance
message_bus = MessageBus()
