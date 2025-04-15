"""
Unit tests for agent communication protocols in ContentFlow AI.
Covers MessageBus and AgentCommunicator for all message types, error cases, and edge conditions.
"""
import asyncio
import pytest
from typing import Any, Dict
# Import from the actual module file, not the directory
from contentflow_ai.src.agents.communication import (
    MessageType, Message, MessageBus, AgentCommunicator
)

@pytest.mark.asyncio
async def test_basic_message_delivery():
    bus = MessageBus()
    received = []
    async def handler(msg: Message):
        received.append(msg)
    bus.subscribe("agent_a", handler)
    msg = Message(
        message_type=MessageType.REQUEST,
        sender="agent_b",
        recipient="agent_a",
        content={"foo": "bar"}
    )
    await bus.publish(msg)
    await asyncio.sleep(0.01)
    assert len(received) == 1
    assert received[0].content == {"foo": "bar"}

@pytest.mark.asyncio
async def test_handler_registration_and_unregistration():
    bus = MessageBus()
    received = []
    async def handler(msg: Message):
        received.append(msg)
    bus.subscribe("agent_x", handler)
    bus.unsubscribe("agent_x", handler)
    msg = Message(
        message_type=MessageType.STATUS,
        sender="agent_y",
        recipient="agent_x",
        content={"status": "ok"}
    )
    await bus.publish(msg)
    await asyncio.sleep(0.01)
    assert len(received) == 0

@pytest.mark.asyncio
async def test_message_correlation():
    bus = MessageBus()
    responses = []
    async def handler(msg: Message):
        if msg.message_type == MessageType.REQUEST:
            resp = Message(
                message_type=MessageType.RESPONSE,
                sender=msg.recipient,
                recipient=msg.sender,
                content={"reply": "pong"},
                in_reply_to=msg.message_id
            )
            await bus.publish(resp)
        elif msg.message_type == MessageType.RESPONSE:
            responses.append(msg)
    bus.subscribe("ping", handler)
    bus.subscribe("pong", handler)
    req = Message(
        message_type=MessageType.REQUEST,
        sender="ping",
        recipient="pong",
        content={"action": "ping"}
    )
    await bus.publish(req)
    await asyncio.sleep(0.05)
    assert any(m.in_reply_to == req.message_id for m in responses)

@pytest.mark.asyncio
async def test_error_handling():
    bus = MessageBus()
    errors = []
    async def handler(msg: Message):
        if msg.message_type == MessageType.REQUEST:
            raise RuntimeError("fail")
        elif msg.message_type == MessageType.ERROR:
            errors.append(msg)
    bus.subscribe("err_agent", handler)
    # Simulate error delivery (should not crash)
    req = Message(
        message_type=MessageType.REQUEST,
        sender="tester",
        recipient="err_agent",
        content={}
    )
    await bus.publish(req)
    await asyncio.sleep(0.01)
    # No error message is sent automatically; test that handler exception is logged but not delivered
    assert len(errors) == 0

@pytest.mark.asyncio
async def test_agent_communicator_send_and_receive():
    bus = MessageBus()
    comm_a = AgentCommunicator("a", "AgentA")
    comm_b = AgentCommunicator("b", "AgentB")
    received = []
    async def on_data(msg: Message):
        received.append(msg)
    comm_b.register_handler(MessageType.DATA, on_data)
    # Patch global message_bus reference
    import contentflow_ai.src.agents.communication as comm_mod
    comm_mod.message_bus = bus
    await comm_a.send_data("b", {"payload": 42})
    await asyncio.sleep(0.01)
    assert len(received) == 1
    assert received[0].content == {"payload": 42}

@pytest.mark.asyncio
async def test_message_history():
    bus = MessageBus()
    async def dummy(msg: Message):
        pass
    bus.subscribe("h1", dummy)
    msg1 = Message(
        message_type=MessageType.STATUS,
        sender="h2",
        recipient="h1",
        content={"status": "test"}
    )
    await bus.publish(msg1)
    history = bus.get_message_history("h1")
    assert any(m.recipient == "h1" for m in history)
