import pytest

from pyamap.api.district import District


def test_district_list_by_keyword(amap):
    place = District(amap)
    result = place.list("成都市")
    assert result


def test_district_list_by_adcode(amap):
    place = District(amap)
    result = place.list("成都市")
    assert result


@pytest.mark.asyncio
async def test_aio_district_list_by_keyword(aio_amap):
    place = District(aio_amap)
    result = await place.list("510100")
    assert result


@pytest.mark.asyncio
async def test_aio_district_list_by_adcode(aio_amap):
    place = District(aio_amap)
    result = await place.list(adcode="510100")
    assert result
