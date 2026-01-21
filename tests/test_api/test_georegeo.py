import pytest

from pyamap.api.georegeo import Georegeo


def test_geo(amap):
    georegeo = Georegeo(amap)
    res = georegeo.geo("成都市天府广场")
    assert res


def test_regeo(amap):
    georegeo = Georegeo(amap)
    res = georegeo.regeo(
        longitude="104.065861",
        latitude="30.657401",
    )
    assert res


@pytest.mark.asyncio
async def test_aio_geo(aio_amap):
    georegeo = Georegeo(aio_amap)
    res = await georegeo.geo("成都市")
    assert res


@pytest.mark.asyncio
async def test_aio_regeo(aio_amap):
    georegeo = Georegeo(aio_amap)
    res = await georegeo.regeo(
        longitude="104.065861",
        latitude="30.657401",
    )
    assert res
