import pytest

from pyamap.api.place import Place


def test_place_text(amap):
    place = Place(amap)
    result = place.text("成都市")
    assert result


def test_place_arround(amap, sample_coordinate):
    place = Place(amap)

    longitude, latitude = sample_coordinate
    result = place.arround("成都市", location=(longitude, latitude))
    assert result


def test_place_polygon(amap, sample_polygon):
    place = Place(amap)
    # 闭合多边形:首尾顶点相同
    ring = [*sample_polygon, sample_polygon[0]]
    result = place.polygon(*ring)
    assert result


def test_place_detai_one_id(amap, sample_ids):
    place = Place(amap)
    one_id = sample_ids[0]
    result = place.detail(one_id)
    assert result


def test_place_detail_multi_id(amap, sample_ids):
    place = Place(amap)
    res = place.detail(*sample_ids)
    assert res


@pytest.mark.asyncio
async def test_aio_place_text(aio_amap):
    place = Place(aio_amap)
    result = await place.text("成都市")
    assert result


@pytest.mark.asyncio
async def test_aio_place_arround(aio_amap, sample_coordinate):
    place = Place(aio_amap)
    longitude, latitude = sample_coordinate
    result = await place.arround("成都市", location=(longitude, latitude))
    assert result


@pytest.mark.asyncio
async def test_aio_place_polygon(aio_amap, sample_polygon):
    place = Place(aio_amap)
    ring = [*sample_polygon, sample_polygon[0]]
    result = await place.polygon(*ring)
    assert result


@pytest.mark.asyncio
async def test_aio_place_detai_one_id(aio_amap, sample_ids):
    place = Place(aio_amap)
    one_id = sample_ids[0]
    result = await place.detail(one_id)
    assert result


@pytest.mark.asyncio
async def test_aio_place_detail_multi_id(aio_amap, sample_ids):
    place = Place(aio_amap)
    result = await place.detail(*sample_ids)
    assert result
