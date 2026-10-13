import pytest

from amap.api.georegeo import Georegeo


def test_geo_includes_address_and_optional_city(sync_client):
    amap, http = sync_client

    Georegeo(amap).geo("天府广场", city="成都")

    assert http.requests[0].path == "/v3/geocode/geo"
    assert http.requests[0].params == {"address": "天府广场", "city": "成都"}


def test_geo_omits_city_when_not_provided(sync_client):
    amap, http = sync_client

    Georegeo(amap).geo("天府广场")

    assert http.requests[0].params == {"address": "天府广场"}


def test_regeo_serializes_optional_api_parameters(sync_client):
    amap, http = sync_client

    Georegeo(amap).regeo(
        ("104.065861", "30.657401"),
        poitype=["050000", "060000"],
        radius=3000,
        extensions="all",
        roadlevel=1,
        homeorcorp=2,
    )

    assert http.requests[0].path == "/v3/geocode/regeo"
    assert http.requests[0].params == {
        "location": "104.065861,30.657401",
        "poitype": "050000|060000",
        "radius": 3000,
        "extensions": "all",
        "roadlevel": 1,
        "homeorcorp": 2,
    }


def test_regeo_omits_optional_fields_and_accepts_zero_radius(sync_client):
    amap, http = sync_client

    Georegeo(amap).regeo(
        ("104", "30"),
        radius=0,
        extensions="base",
        roadlevel=None,
        homeorcorp=None,
    )

    assert http.requests[0].params == {
        "location": "104,30",
        "radius": 0,
        "extensions": "base",
    }


@pytest.mark.parametrize("radius", [-1, 3001])
def test_regeo_rejects_radius_outside_documented_range(sync_client, radius):
    amap, http = sync_client

    with pytest.raises(ValueError):
        Georegeo(amap).regeo(("104", "30"), radius=radius)

    assert http.requests == []


@pytest.mark.asyncio
async def test_geo_and_regeo_support_async_http_client(async_client):
    amap, http = async_client

    assert (await Georegeo(amap).geo("天府广场"))["status"] == "1"
    assert (await Georegeo(amap).regeo(("104", "30")))["status"] == "1"
    assert [request.path for request in http.requests] == [
        "/v3/geocode/geo",
        "/v3/geocode/regeo",
    ]
