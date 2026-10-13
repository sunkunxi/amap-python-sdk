import pytest

from pyamap.api.weather import Weather


def test_info_sends_city_and_default_output(sync_client):
    amap, http = sync_client

    Weather(amap).info("510100")

    assert http.requests[0].path == "/v3/weather/weatherInfo"
    assert http.requests[0].params == {"city": "510100", "output": "JSON"}


def test_info_sends_extensions_and_output_separately(sync_client):
    amap, http = sync_client

    Weather(amap).info("510100", extensions="all", output="xml")

    assert http.requests[0].params == {
        "city": "510100",
        "extensions": "all",
        "output": "XML",
    }


@pytest.mark.asyncio
async def test_info_supports_async_http_client(async_client):
    amap, http = async_client

    result = await Weather(amap).info("510100")

    assert result["status"] == "1"
    assert http.requests[0].path == "/v3/weather/weatherInfo"
