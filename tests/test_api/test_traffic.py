import pytest

from pyamap.api.traffic import Traffic


def test_circle_traffic_formats_location_and_options(sync_client):
    amap, http = sync_client

    Traffic(amap).circle(
        1,
        ("104.07", "30.66"),
        radius=4999,
        extensions="all",
        sig="signature",
        output="xml",
    )

    assert http.requests[0].path == "/v3/traffic/status/circle"
    assert http.requests[0].params == {
        "level": 1,
        "location": "104.07,30.66",
        "radius": 4999,
        "extensions": "all",
        "output": "XML",
        "sig": "signature",
    }


@pytest.mark.parametrize("radius", [0, 5000])
def test_circle_rejects_radius_out_of_range(sync_client, radius):
    amap, http = sync_client

    with pytest.raises(ValueError):
        Traffic(amap).circle(1, ("104", "30"), radius=radius)

    assert http.requests == []


def test_rectangle_traffic_uses_semicolon_between_corners(sync_client):
    amap, http = sync_client

    Traffic(amap).rectangle(
        4,
        (("104", "30"), ("105", "31")),
    )

    assert http.requests[0].path == "/v3/traffic/status/rectangle"
    assert http.requests[0].params == {
        "level": 4,
        "rectangle": "104,30;105,31",
        "extensions": "base",
        "output": "JSON",
    }
    Traffic(amap).rectangle(
        4,
        (("104", "30"), ("105", "31")),
        sig="signature",
    )
    assert http.requests[1].params["sig"] == "signature"


def test_road_requires_city_or_adcode_and_accepts_either(sync_client):
    amap, http = sync_client

    with pytest.raises(ValueError):
        Traffic(amap).road(1, "人民路")
    assert http.requests == []

    Traffic(amap).road(
        1,
        "人民路",
        adcode="510100",
        city="成都",
        sig="signature",
    )

    assert http.requests[0].path == "/v3/traffic/status/road"
    assert http.requests[0].params["city"] == "成都"
    assert http.requests[0].params["adcode"] == "510100"
    assert http.requests[0].params["sig"] == "signature"


@pytest.mark.asyncio
async def test_traffic_endpoints_support_async_http_client(async_client):
    amap, http = async_client

    await Traffic(amap).circle(1, ("104", "30"))
    await Traffic(amap).rectangle(1, (("104", "30"), ("105", "31")))
    await Traffic(amap).road(1, "人民路", city="成都")

    assert len(http.requests) == 3
