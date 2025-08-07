import pytest

from pyamap.api.place import Place


def test_place_text(amap):
    place = Place(amap)
    res = place.text("成都市")
    assert res.json()


def test_place_arround(amap):
    place = Place(amap)
    res = place.arround("成都市", longitude="116.407082", latitude="39.910464")
    assert res.json()


def test_place_polygon(amap):
    place = Place(amap)
    res = place.polygon(("1", "2"), ("3", "4"))
    assert res.json()


def test_place_detail(amap):
    place = Place(amap)
    res = place.detail("ABSC", "A")
    assert res.json()


@pytest.mark.asyncio
async def test_aio_place_text(aio_amap):
    place = Place(aio_amap)
    res = await place.text("成都市")
    assert res


@pytest.mark.asyncio
async def test_aio_place_arround(aio_amap):
    place = Place(aio_amap)
    res = await place.arround("成都市", longitude="116.407082", latitude="39.910464")
    assert res


@pytest.mark.asyncio
async def test_aio_place_polygon(aio_amap):
    place = Place(aio_amap)
    res = await place.polygon(("1", "2"), ("3", "4"))
    assert res
    print(res)


@pytest.mark.asyncio
async def test_aio_place_detail(aio_amap):
    place = Place(aio_amap)
    res = await place.detail("ABSC", "A")
    assert res
    print(res)
