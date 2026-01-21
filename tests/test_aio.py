import pytest

from pyamap.aio import HTTPClient
from pyamap.api.district import District
from pyamap.api.place import Place
from pyamap.api.weather import Weather
from pyamap.api.georegeo import Georegeo

@pytest.mark.asyncio
async def test_amap_init(aio_amap):
    assert aio_amap


@pytest.mark.asyncio
async def test_amap_http_client(aio_amap):
    assert aio_amap.http and isinstance(aio_amap.http, HTTPClient)


@pytest.mark.asyncio
async def test_amap_api_agent(aio_amap):
    assert aio_amap.http is not None and isinstance(aio_amap.http, HTTPClient)
    assert aio_amap.place and isinstance(aio_amap.place, Place)
    assert aio_amap.weather and isinstance(aio_amap.weather, Weather)
    assert aio_amap.district and isinstance(aio_amap.district, District)


@pytest.mark.asyncio
async def test_amap_api_agent_initiailize(aio_amap2):
    assert aio_amap2.http is not None and isinstance(aio_amap2.http, HTTPClient)
    assert aio_amap2.place and isinstance(aio_amap2.place, Place)
    assert aio_amap2.weather and isinstance(aio_amap2.weather, Weather)
    assert aio_amap2.district and isinstance(aio_amap2.district, District)
    assert aio_amap2.georegeo and isinstance(aio_amap2.georegeo, Georegeo)
