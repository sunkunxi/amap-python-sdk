import logging
from unittest.mock import AsyncMock, Mock

import aiohttp
import pytest
import requests

from amap import AmapAPIError, AmapTimeoutError, base
from amap.aio import HTTPClient as AsyncHTTPClient
from amap.amap import HTTPClient as SyncHTTPClient


@pytest.mark.parametrize("method", ["get", "put", "delete", "post"])
def test_sync_http_client_forwards_request_and_injects_key(monkeypatch, method):
    session = Mock()
    session.request.return_value.json.return_value = {"status": "1"}
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
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
    session.request.assert_called_once_with(
        method.upper(),
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
    session.request.return_value.json.assert_called_once_with()


def test_sync_http_client_logs_safe_success_details(caplog, monkeypatch):
    session = Mock()
    session.request.return_value.status_code = 200
    session.request.return_value.json.return_value = {"status": "1"}
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("secret-api-key", "https://example.test")

    with caplog.at_level(logging.DEBUG, logger="amap.amap"):
        client.get("/v3/place/text", params={"keywords": "private place"})

    assert "Amap request succeeded" in caplog.text
    assert "/v3/place/text" in caplog.text
    assert "status_code=200" in caplog.text
    assert "duration_ms=" not in caplog.text
    assert "secret-api-key" not in caplog.text
    assert "private place" not in caplog.text


def test_sync_http_client_close_and_exceptions_propagate(monkeypatch):
    session = Mock()
    session.request.side_effect = RuntimeError("transport failure")
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("key", "https://example.test")

    with pytest.raises(RuntimeError, match="transport failure"):
        client.get("/path", params={})

    client.close()
    session.close.assert_called_once_with()


def test_sync_http_client_logs_connection_failures_without_exception_text(caplog, monkeypatch):
    session = Mock()
    session.request.side_effect = requests.exceptions.ConnectionError("private url")
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("key", "https://example.test")

    with caplog.at_level(logging.WARNING, logger="amap.amap"):
        with pytest.raises(requests.exceptions.ConnectionError, match="private url"):
            client.get("/path", params={})

    assert "Amap HTTP request failed" in caplog.text
    assert "error_type=ConnectionError" in caplog.text
    assert "private url" not in caplog.text


@pytest.mark.parametrize("method", ["get", "put", "delete", "post"])
def test_sync_http_client_raises_amap_api_error(caplog, monkeypatch, method):
    response = Mock()
    response.json.return_value = {
        "status": "0",
        "info": "USERKEY_PLAT_NOMATCH",
        "infocode": "10001",
    }
    session = Mock()
    session.request.return_value = response
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("key", "https://example.test")

    with caplog.at_level(logging.WARNING, logger="amap.amap"):
        with pytest.raises(AmapAPIError) as exc_info:
            getattr(client, method)("/path", params={})

    assert exc_info.value.infocode == "10001"
    assert exc_info.value.info == "USERKEY_PLAT_NOMATCH"
    assert exc_info.value.response == response.json.return_value
    assert "infocode=10001" in caplog.text
    assert "key" not in caplog.text


@pytest.mark.parametrize("method", ["get", "put", "delete", "post"])
def test_sync_http_client_converts_request_timeouts(monkeypatch, method):
    session = Mock()
    session.request.side_effect = requests.exceptions.Timeout("slow")
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("key", "https://example.test")

    with pytest.raises(AmapTimeoutError, match="Amap request timed out") as exc_info:
        getattr(client, method)("/path", params={})

    assert isinstance(exc_info.value.__cause__, requests.exceptions.Timeout)


@pytest.mark.parametrize("method", ["get", "put", "delete", "post", "close"])
def test_abstract_http_client_methods_raise_not_implemented(monkeypatch, method):
    session = Mock()
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
    client = SyncHTTPClient("key", "https://example.test")

    with pytest.raises(NotImplementedError):
        (
            getattr(base.HTTPClient, method)(client, "/path", params={})
            if method != "close"
            else getattr(base.HTTPClient, method)(client)
        )


def test_abstract_amap_http_property_raises_not_implemented(monkeypatch):
    session = Mock()
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)
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
    monkeypatch.setattr("amap.aio.aiohttp.TCPConnector", lambda limit: ("connector", limit))
    monkeypatch.setattr(
        "amap.aio.aiohttp.ClientSession",
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
    monkeypatch.setattr("amap.aio.aiohttp.TCPConnector", lambda limit: None)
    monkeypatch.setattr("amap.aio.aiohttp.ClientSession", lambda connector: session)
    client = AsyncHTTPClient("key", "https://example.test", max_connector=1)

    with pytest.raises(RuntimeError, match="transport failure"):
        await client.get("/path", params={})

    session.close = Mock(return_value=_awaitable(None))
    await client.close()
    session.close.assert_called_once_with()


@pytest.mark.asyncio
async def test_async_http_client_logs_connection_failures_without_exception_text(
    caplog, monkeypatch
):
    session = Mock()
    session.request = Mock(side_effect=_async_error(aiohttp.ClientError("private url")))
    monkeypatch.setattr("amap.aio.aiohttp.TCPConnector", lambda limit: None)
    monkeypatch.setattr("amap.aio.aiohttp.ClientSession", lambda connector: session)
    client = AsyncHTTPClient("key", "https://example.test", max_connector=1)

    with caplog.at_level(logging.WARNING, logger="amap.aio"):
        with pytest.raises(aiohttp.ClientError, match="private url"):
            await client.get("/path", params={})

    assert "Amap HTTP request failed" in caplog.text
    assert "error_type=ClientError" in caplog.text
    assert "private url" not in caplog.text


@pytest.mark.asyncio
async def test_async_http_client_raises_amap_api_error(caplog, monkeypatch):
    response = Mock()
    response.json = AsyncMock(
        return_value={
            "status": "0",
            "info": "USERKEY_PLAT_NOMATCH",
            "infocode": "10001",
        }
    )
    session = Mock()
    session.request = Mock(return_value=_awaitable(response))
    monkeypatch.setattr("amap.aio.aiohttp.TCPConnector", lambda limit: None)
    monkeypatch.setattr("amap.aio.aiohttp.ClientSession", lambda connector: session)
    client = AsyncHTTPClient("key", "https://example.test", max_connector=1)

    with caplog.at_level(logging.WARNING, logger="amap.aio"):
        with pytest.raises(AmapAPIError) as exc_info:
            await client.get("/path", params={})

    assert exc_info.value.infocode == "10001"
    assert exc_info.value.info == "USERKEY_PLAT_NOMATCH"
    assert "infocode=10001" in caplog.text
    assert "key" not in caplog.text


@pytest.mark.asyncio
async def test_async_http_client_converts_request_timeouts(monkeypatch):
    session = Mock()
    session.request = Mock(side_effect=_async_error(TimeoutError("slow")))
    monkeypatch.setattr("amap.aio.aiohttp.TCPConnector", lambda limit: None)
    monkeypatch.setattr("amap.aio.aiohttp.ClientSession", lambda connector: session)
    client = AsyncHTTPClient("key", "https://example.test", max_connector=1)

    with pytest.raises(AmapTimeoutError, match="Amap request timed out") as exc_info:
        await client.get("/path", params={})

    assert isinstance(exc_info.value.__cause__, TimeoutError)


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
