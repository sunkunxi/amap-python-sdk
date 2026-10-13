from unittest.mock import AsyncMock, Mock

import pytest

from pyamap import base
from pyamap.aio import HTTPClient as AsyncHTTPClient
from pyamap.amap import HTTPClient as SyncHTTPClient


@pytest.mark.parametrize("method", ["get", "put", "delete", "post"])
def test_sync_http_client_forwards_request_and_injects_key(monkeypatch, method):
    session = Mock()
    session_method = getattr(session, method)
    session_method.return_value.json.return_value = {"status": "1"}
    monkeypatch.setattr("pyamap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("secret", "https://example.test")
    params = {"city": "510100", "citylimit": True, "disabled": False}
    headers = {"X-Test": "value"}

    result = getattr(client, method)(
        "/v3/weather/weatherInfo",
        params=params,
        data="payload",
        headers=headers,
    )

    assert result == {"status": "1"}
    session_method.assert_called_once_with(
        "https://example.test/v3/weather/weatherInfo",
        params={
            "city": "510100",
            "citylimit": "true",
            "disabled": "false",
            "key": "secret",
        },
        headers=headers,
        data="payload",
    )
    session_method.return_value.json.assert_called_once_with()


def test_sync_http_client_close_and_exceptions_propagate(monkeypatch):
    session = Mock()
    session.get.side_effect = RuntimeError("transport failure")
    monkeypatch.setattr("pyamap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("key", "https://example.test")

    with pytest.raises(RuntimeError, match="transport failure"):
        client.get("/path", params={})

    client.close()
    session.close.assert_called_once_with()


@pytest.mark.parametrize("method", ["get", "put", "delete", "post", "close"])
def test_abstract_http_client_methods_raise_not_implemented(monkeypatch, method):
    session = Mock()
    monkeypatch.setattr("pyamap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("key", "https://example.test")

    with pytest.raises(NotImplementedError):
        (
            getattr(base.HTTPClient, method)(client, "/path", params={})
            if method != "close"
            else getattr(base.HTTPClient, method)(client)
        )


def test_abstract_amap_http_property_raises_not_implemented(monkeypatch):
    session = Mock()
    monkeypatch.setattr("pyamap.amap.requests.Session", lambda: session)
    amap = SyncHTTPClient("key", "https://example.test")

    with pytest.raises(NotImplementedError):
        base.Amap.http.fget(amap)


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["get", "put", "delete", "post"])
async def test_async_http_client_forwards_request_and_normalizes_bools(monkeypatch, method):
    response = Mock()
    response.json = AsyncMock(return_value={"status": "1"})
    session = Mock()
    session.request = Mock(return_value=_awaitable(response))
    monkeypatch.setattr("pyamap.aio.aiohttp.TCPConnector", lambda limit: ("connector", limit))
    monkeypatch.setattr(
        "pyamap.aio.aiohttp.ClientSession",
        lambda connector: _session_holder(session, connector),
    )
    client = AsyncHTTPClient("secret", "https://example.test", max_connector=12)
    params = {"citylimit": True, "disabled": False}
    headers = {"X-Test": "value"}

    result = await getattr(client, method)(
        "/v3/place/text",
        params=params,
        data="payload",
        headers=headers,
    )

    assert result == {"status": "1"}
    session.request.assert_called_once_with(
        method.upper(),
        "https://example.test/v3/place/text",
        params={"citylimit": "true", "disabled": "false", "key": "secret"},
        headers=headers,
        data="payload",
    )
    response.json.assert_called_once_with()


@pytest.mark.asyncio
async def test_async_http_client_propagates_errors_and_closes(monkeypatch):
    session = Mock()
    session.request = Mock(side_effect=_async_error(RuntimeError("transport failure")))
    monkeypatch.setattr("pyamap.aio.aiohttp.TCPConnector", lambda limit: None)
    monkeypatch.setattr("pyamap.aio.aiohttp.ClientSession", lambda connector: session)
    client = AsyncHTTPClient("key", "https://example.test", max_connector=1)

    with pytest.raises(RuntimeError, match="transport failure"):
        await client.get("/path", params={})

    session.close = Mock(return_value=_awaitable(None))
    await client.close()
    session.close.assert_called_once_with()


def _awaitable(value):
    async def resolve():
        return value

    return resolve()


def _async_error(error):
    async def raise_error(*args, **kwargs):
        raise error

    return raise_error


def _session_holder(session, connector):
    assert connector == ("connector", 12)
    return session
