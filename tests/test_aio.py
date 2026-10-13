import asyncio
from unittest.mock import Mock

import pytest

from amap.aio import Amap


def test_async_amap_requires_initialization_and_can_be_awaited(monkeypatch):
    http = Mock()
    factory = Mock(return_value=http)
    monkeypatch.setattr("amap.aio.HTTPClient", factory)
    amap = Amap("key", max_connector=7)

    with pytest.raises(RuntimeError, match="not initialized"):
        _ = amap.http

    async def initialize():
        return await amap

    assert asyncio.run(initialize()) is amap
    assert amap.http is http
    factory.assert_called_once_with(
        "key",
        "https://restapi.amap.com",
        max_connector=7,
    )


def test_async_context_closes_client_even_when_body_raises(monkeypatch):
    http = Mock()
    http.close = Mock(return_value=_awaitable(None))
    monkeypatch.setattr("amap.aio.HTTPClient", lambda *args, **kwargs: http)
    amap = Amap("key")

    async def raise_inside_context():
        async with amap:
            raise RuntimeError("body failure")

    with pytest.raises(RuntimeError, match="body failure"):
        asyncio.run(raise_inside_context())

    http.close.assert_called_once_with()


def _awaitable(value):
    async def resolve():
        return value

    return resolve()
