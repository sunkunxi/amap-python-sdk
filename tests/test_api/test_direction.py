import pytest

from pyamap.api.direction import Direction


# ---------------------------------------------------------------- #
# 同步
# ---------------------------------------------------------------- #
def test_direction_walking(amap):
    direction = Direction(amap)
    res = direction.walking(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
    )
    assert res


def test_direction_walking_with_show_fields(amap):
    direction = Direction(amap)
    res = direction.walking(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        show_fields=["cost", "navi", "polyline"],
        alternative_route=2,
    )
    assert res


def test_direction_driving(amap):
    direction = Direction(amap)
    res = direction.driving(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
    )
    assert res


def test_direction_driving_strategy_32(amap):
    """32 = 高德推荐(默认策略,返回多条备选)"""
    direction = Direction(amap)
    res = direction.driving(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        strategy=32,
        show_fields=["cost", "cities"],
    )
    assert res


def test_direction_driving_with_waypoints(amap):
    direction = Direction(amap)
    res = direction.driving(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        waypoints=[("104.07", "30.67"), ("104.07", "30.68")],
    )
    assert res


def test_direction_driving_with_avoidpolygons(amap):
    direction = Direction(amap)
    avoid = [
        [
            ("104.06", "30.68"),
            ("104.06", "30.66"),
            ("104.08", "30.66"),
            ("104.08", "30.68"),
        ]
    ]
    res = direction.driving(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        avoidpolygons=avoid,
    )
    assert res


def test_direction_driving_with_plate(amap):
    """v5:车牌号改为 plate 单字段"""
    direction = Direction(amap)
    res = direction.driving(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        plate="京AHA322",
    )
    assert res


def test_direction_transit(amap):
    """v5:city1/city2 替代 city/cityd"""
    direction = Direction(amap)
    res = direction.transit(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        city1="010",  # 北京;成都用 028
    )
    assert res


def test_direction_bicycling(amap):
    direction = Direction(amap)
    res = direction.bicycling(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        alternative_route=2,
    )
    assert res


def test_direction_electrobike(amap):
    """v5 新增:电动车路径规划"""
    direction = Direction(amap)
    res = direction.electrobike(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
    )
    assert res


# ---------------------------------------------------------------- #
# 异步
# ---------------------------------------------------------------- #
@pytest.mark.asyncio
async def test_aio_direction_walking(aio_amap):
    direction = Direction(aio_amap)
    res = await direction.walking(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
    )
    assert res


@pytest.mark.asyncio
async def test_aio_direction_driving(aio_amap):
    direction = Direction(aio_amap)
    res = await direction.driving(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
        strategy=32,
    )
    assert res


@pytest.mark.asyncio
async def test_aio_direction_electrobike(aio_amap):
    direction = Direction(aio_amap)
    res = await direction.electrobike(
        origin=("104.07", "30.66"),
        destination=("104.07", "30.69"),
    )
    assert res
