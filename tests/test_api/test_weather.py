import pytest

from pyamap.api.weather import Weather


def test_weather_info(amap):
    weather = Weather(amap)
    res = weather.info("成都市")
    assert res.json()
    print(res.json())


@pytest.mark.asyncio
async def test_aio_weather_info(aio_amap):
    weather = Weather(aio_amap)
    res = await weather.info("成都市")
    assert res
