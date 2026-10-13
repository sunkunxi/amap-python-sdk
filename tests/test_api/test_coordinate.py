import pytest

from pyamap.api.coordinate import Coordinate


def test_coordinate_convert_from_gps(amap):
    coordinate = Coordinate(amap)
    res = coordinate.convert(
        locations=[("116.481499", "39.990475")],
        coordsys="gps",
    )
    assert res


def test_coordinate_convert_from_baidu(amap):
    coordinate = Coordinate(amap)
    res = coordinate.convert(
        locations=[("116.481499", "39.990475")],
        coordsys="baidu",
    )
    assert res


def test_coordinate_convert_many(amap):
    coordinate = Coordinate(amap)
    res = coordinate.convert(
        locations=[
            ("116.481499", "39.990475"),
            ("116.457400", "39.910400"),
        ],
        coordsys="gps",
    )
    assert res


@pytest.mark.asyncio
async def test_aio_coordinate_convert(aio_amap):
    coordinate = Coordinate(aio_amap)
    res = await coordinate.convert(
        locations=[("116.481499", "39.990475")],
        coordsys="gps",
    )
    assert res
