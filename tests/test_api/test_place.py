import pytest

from pyamap.api.place import Place


def test_place_text(amap):
    place = Place(amap)
    res = place.text("成都市")
    assert res


def test_place_arround(amap, sample_coordinate):
    place = Place(amap)

    longitude, latitude = sample_coordinate
    res = place.arround("成都市", longitude=longitude, latitude=latitude)
    assert res


def test_place_polygon(amap, sample_polygon):
    place = Place(amap)
    res = place.polygon(*sample_polygon)
    assert res


def test_place_detai_one_id(amap, sample_ids):
    place = Place(amap)
    one_id = sample_ids[0]
    res = place.detail(one_id)
    assert res


def test_place_detail_multi_id(amap, sample_ids):
    place = Place(amap)
    res = place.detail(*sample_ids)
    assert res


@pytest.mark.asyncio
async def test_aio_place_text(aio_amap):
    place = Place(aio_amap)
    res = await place.text("成都市")
    assert res


@pytest.mark.asyncio
async def test_aio_place_arround(aio_amap, sample_coordinate):
    place = Place(aio_amap)
    longitude, latitude = sample_coordinate
    res = await place.arround("成都市", longitude=longitude, latitude=latitude)
    assert res


@pytest.mark.asyncio
async def test_aio_place_polygon(aio_amap, sample_polygon):
    place = Place(aio_amap)
    result = await place.polygon(*sample_polygon)
    data = await result.json()
    assert data


@pytest.mark.asyncio
async def test_aio_place_detai_one_id(aio_amap, sample_ids):
    place = Place(aio_amap)
    one_id = sample_ids[0]
    result = await place.detail(one_id)
    data = await result.json()
    assert data


@pytest.mark.asyncio
async def test_aio_place_detail_multi_id(aio_amap, sample_ids):
    place = Place(aio_amap)
    result = await place.detail(*sample_ids)
    data = await result.json()
    assert data
