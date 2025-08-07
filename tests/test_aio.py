import pytest

from pyamap.aio import HTTPClient
from pyamap.api.place import Place
from pyamap.api.weather import Weather


@pytest.mark.asyncio
async def test_amap_init(aio_amap):
    assert aio_amap


@pytest.mark.asyncio
async def test_amap_http_client(aio_amap):
    assert aio_amap.http and isinstance(aio_amap.http, HTTPClient)


@pytest.mark.asyncio
async def test_amap_api_agent(aio_amap):
    assert aio_amap.place and isinstance(aio_amap.place, Place)
    assert aio_amap.weather and isinstance(aio_amap.weather, Weather)
