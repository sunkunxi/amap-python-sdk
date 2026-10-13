import pytest

from pyamap.api.distance import Distance


def test_distance_measure(amap, sample_coordinate):
    distance = Distance(amap)
    longitude, latitude = sample_coordinate
    res = distance.measure(
        origins=[(longitude, latitude)],
        destination=("104.07", "30.69"),
        type=0,
    )
    assert res


def test_distance_measure_many_to_one(amap, sample_coordinate):
    distance = Distance(amap)
    longitude, latitude = sample_coordinate
    res = distance.measure(
        origins=[(longitude, latitude), ("104.08", "30.66")],
        destination=("104.07", "30.69"),
        type=0,
    )
    assert res


@pytest.mark.asyncio
async def test_aio_distance_measure(aio_amap, sample_coordinate):
    distance = Distance(aio_amap)
    longitude, latitude = sample_coordinate
    res = await distance.measure(
        origins=[(longitude, latitude)],
        destination=("104.07", "30.69"),
    )
    assert res
