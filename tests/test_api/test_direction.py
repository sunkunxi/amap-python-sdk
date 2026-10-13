import pytest

from amap.api.direction import Direction


def test_walking_formats_coordinates_and_fields(sync_client):
    amap, http = sync_client

    Direction(amap).walking(
        ("104", "30"),
        ("105", "31"),
        origin_id="start",
        destination_id="end",
        alternative_route=2,
        show_fields=["cost", "polyline"],
        isindoor=1,
        sig="signature",
        callback="handler",
    )

    assert http.requests[0].path == "/v5/direction/walking"
    assert http.requests[0].params == {
        "origin": "104,30",
        "destination": "105,31",
        "isindoor": 1,
        "output": "JSON",
        "origin_id": "start",
        "destination_id": "end",
        "alternative_route": 2,
        "show_fields": "cost,polyline",
        "sig": "signature",
        "callback": "handler",
    }


def test_transit_serializes_all_optional_fields(sync_client):
    amap, http = sync_client

    Direction(amap).transit(
        ("104", "30"),
        ("105", "31"),
        "成都",
        city2="重庆",
        originpoi="start",
        destinationpoi="end",
        ad1="510100",
        ad2="500000",
        strategy=2,
        alternative_route=3,
        nightflag=1,
        date="2026-01-01",
        time="9",
        show_fields=["cost", "navi"],
        sig="signature",
        callback="handler",
    )

    assert http.requests[0].path == "/v5/direction/transit/integrated"
    assert http.requests[0].params == {
        "origin": "104,30",
        "destination": "105,31",
        "city1": "成都",
        "output": "JSON",
        "city2": "重庆",
        "originpoi": "start",
        "destinationpoi": "end",
        "ad1": "510100",
        "ad2": "500000",
        "strategy": 2,
        "AlternativeRoute": 3,
        "nightflag": 1,
        "date": "2026-01-01",
        "time": "9",
        "show_fields": "cost,navi",
        "sig": "signature",
        "callback": "handler",
    }


def test_driving_serializes_routes_and_avoid_polygons(sync_client):
    amap, http = sync_client

    Direction(amap).driving(
        ("104", "30"),
        ("105", "31"),
        destination_type="0101",
        origin_id="start",
        destination_id="end",
        strategy=33,
        waypoints=[("104.1", "30.1"), ("104.2", "30.2")],
        avoidpolygons=[[("1", "1"), ("2", "2")], [("3", "3"), ("4", "4")]],
        plate="川A12345",
        cartype=1,
        ferry=0,
        show_fields=["cost", "tmcs"],
        sig="signature",
        callback="handler",
    )

    assert http.requests[0].path == "/v5/direction/driving"
    assert http.requests[0].params == {
        "origin": "104,30",
        "destination": "105,31",
        "output": "JSON",
        "destination_type": "0101",
        "origin_id": "start",
        "destination_id": "end",
        "strategy": 33,
        "waypoints": "104.1,30.1;104.2,30.2",
        "avoidpolygons": "1,1;2,2|3,3;4,4",
        "plate": "川A12345",
        "cartype": 1,
        "ferry": 0,
        "show_fields": "cost,tmcs",
        "sig": "signature",
        "callback": "handler",
    }


def test_driving_obeys_documented_waypoint_and_polygon_limits(sync_client):
    amap, http = sync_client
    points = [("1", "1")] * 17

    with pytest.raises(ValueError):
        Direction(amap).driving(("1", "1"), ("2", "2"), waypoints=points)
    with pytest.raises(ValueError):
        Direction(amap).driving(("1", "1"), ("2", "2"), avoidpolygons=[[("1", "1")]] * 33)

    assert http.requests == []


@pytest.mark.parametrize(
    "method,path",
    [
        ("bicycling", "/v5/direction/bicycling"),
        ("electrobike", "/v5/direction/electrobike"),
    ],
)
def test_two_wheel_modes_share_parameter_shape(sync_client, method, path):
    amap, http = sync_client

    getattr(Direction(amap), method)(
        ("104", "30"),
        ("105", "31"),
        alternative_route=3,
        show_fields=["cost", "polyline"],
        sig="signature",
        callback="handler",
    )

    assert http.requests[0].path == path
    assert http.requests[0].params == {
        "origin": "104,30",
        "destination": "105,31",
        "output": "JSON",
        "alternative_route": 3,
        "show_fields": "cost,polyline",
        "sig": "signature",
        "callback": "handler",
    }


@pytest.mark.asyncio
async def test_all_direction_modes_support_async_http_client(async_client):
    amap, http = async_client
    direction = Direction(amap)

    await direction.walking(("1", "1"), ("2", "2"))
    await direction.transit(("1", "1"), ("2", "2"), "成都")
    await direction.driving(("1", "1"), ("2", "2"))
    await direction.bicycling(("1", "1"), ("2", "2"))
    await direction.electrobike(("1", "1"), ("2", "2"))

    assert len(http.requests) == 5
