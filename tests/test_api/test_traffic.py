import pytest

from pyamap.api.traffic import Traffic


def test_traffic_circle(amap, sample_coordinate):
    traffic = Traffic(amap)
    longitude, latitude = sample_coordinate
    res = traffic.circle(
        level=5,
        location=(longitude, latitude),
        radius=1500,
    )
    assert res


def test_traffic_rectangle(amap, sample_polygon):
    traffic = Traffic(amap)
    res = traffic.rectangle(
        level=5,
        rectangle=(sample_polygon[0], sample_polygon[1]),
    )
    assert res


def test_traffic_road(amap):
    traffic = Traffic(amap)
    res = traffic.road(
        level=5,
        name="人民南路",
        adcode="510100",
    )
    assert res


@pytest.mark.asyncio
async def test_aio_traffic_circle(aio_amap, sample_coordinate):
    traffic = Traffic(aio_amap)
    longitude, latitude = sample_coordinate
    res = await traffic.circle(
        level=5,
        location=(longitude, latitude),
    )
    assert res
