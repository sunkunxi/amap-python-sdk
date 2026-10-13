import pytest

from pyamap.api.inputtips import InputTips


def test_inputtips_query(amap):
    inputtips = InputTips(amap)
    res = inputtips.query("成都市")
    assert res


def test_inputtips_with_city(amap):
    inputtips = InputTips(amap)
    res = inputtips.query("天府广场", city="成都")
    assert res


def test_inputtips_with_location(amap, sample_coordinate):
    inputtips = InputTips(amap)
    longitude, latitude = sample_coordinate
    res = inputtips.query("咖啡", location=(longitude, latitude))
    assert res


@pytest.mark.asyncio
async def test_aio_inputtips_query(aio_amap):
    inputtips = InputTips(aio_amap)
    res = await inputtips.query("成都市")
    assert res
