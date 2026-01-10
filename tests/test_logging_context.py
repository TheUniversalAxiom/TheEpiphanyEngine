"""
Tests for logging context isolation using contextvars.
"""

import asyncio

from web.logging_config import LogContext, get_request_id, get_user


def test_context_isolation_between_tasks():
    async def capture_context(request_id, user, delay):
        with LogContext(request_id=request_id, user=user):
            await asyncio.sleep(delay)
            return get_request_id(), get_user()

    async def run_tasks():
        task_one = asyncio.create_task(capture_context("req-1", "alice", 0.05))
        task_two = asyncio.create_task(capture_context("req-2", "bob", 0.01))
        return await asyncio.gather(task_one, task_two)

    results = asyncio.run(run_tasks())

    assert results == [("req-1", "alice"), ("req-2", "bob")]
    assert get_request_id() is None
    assert get_user() is None
