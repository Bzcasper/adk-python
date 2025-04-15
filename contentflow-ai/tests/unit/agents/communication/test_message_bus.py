import os
import sys
import pytest
from dotenv import load_dotenv

load_dotenv()

"""Unit tests for MessageBus and AgentMessage in ContentFlow AI."""
import asyncio
import os
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../src'))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
from agents.communication.message_bus import MessageBus, AgentMessage, MessageType

@pytest.mark.asyncio
async def test_message_bus_send_and_receive():
    bus = MessageBus()
    received = {}

    async def handler(msg: AgentMessage):
        received['msg'] = msg

    await bus.register_agent('agent_a', handler)
    await bus.register_agent('agent_b', handler)

    message = MessageBus.create_message(
        sender='agent_a',
        recipient='agent_b',
        type=MessageType.REQUEST,
        payload={'data': 'hello'}
    )

    # Start listening in background
    listener = asyncio.create_task(bus.listen('agent_b'))
    await bus.send_message(message)

    # Give some time for handler to process
    await asyncio.sleep(0.1)
    listener.cancel()
    assert 'msg' in received
    assert received['msg'].sender == 'agent_a'
    assert received['msg'].recipient == 'agent_b'
    assert received['msg'].type == MessageType.REQUEST
    assert received['msg'].payload['data'] == 'hello'

@pytest.mark.asyncio
async def test_message_bus_unregistered_agent():
    bus = MessageBus()
    message = MessageBus.create_message(
        sender='agent_a',
        recipient='agent_x',
        type=MessageType.REQUEST,
        payload={}
    )
    with pytest.raises(ValueError):
        await bus.send_message(message)

@pytest.mark.asyncio
async def test_message_bus_no_handler():
    bus = MessageBus()
    # Register agent without handler
    await bus.register_agent('agent_b', None)
    message = MessageBus.create_message(
        sender='agent_a',
        recipient='agent_b',
        type=MessageType.REQUEST,
        payload={}
    )
    listener = asyncio.create_task(bus.listen('agent_b'))
    await bus.send_message(message)
    await asyncio.sleep(0.1)
    listener.cancel()
    # No exception should be raised if no handler

@pytest.mark.asyncio
async def test_message_bus_error_in_handler():
    bus = MessageBus()
    async def handler(msg):
        raise RuntimeError('handler error')
    await bus.register_agent('agent_b', handler)
    message = MessageBus.create_message(
        sender='agent_a',
        recipient='agent_b',
        type=MessageType.REQUEST,
        payload={}
    )
    listener = asyncio.create_task(bus.listen('agent_b'))
    await bus.send_message(message)
    await asyncio.sleep(0.1)
    listener.cancel()
    # Should log error but not crash
