import pytest

from pyamap.api.coordinate import Coordinate
from pyamap.types import Coordinate as CoordinatePair


def test_convert_formats_locations_and_optional_params(sync_client):
    amap, http = sync_client

    result = Coordinate(amap).convert(
        [("116.481499", "39.990475"), ("116.457400", "39.910400")],
        coordsys="gps",
        sig="signature",
        output="xml",
    )

    assert result == {"status": "1", "info": "OK"}
    assert http.requests[0].path == "/v3/assistant/coordinate/convert"
    assert http.requests[0].params == {
        "locations": "116.481499,39.990475|116.457400,39.910400",
        "coordsys": "gps",
        "output": "XML",
        "sig": "signature",
    }


def test_convert_uses_autonavi_and_json_defaults(sync_client):
    amap, http = sync_client

    Coordinate(amap).convert([("104.07", "30.66")])

    assert http.requests[0].params == {
        "locations": "104.07,30.66",
        "coordsys": "autonavi",
        "output": "JSON",
    }


def test_convert_accepts_documented_maximum_of_40_locations(sync_client):
    amap, http = sync_client
    locations: list[CoordinatePair] = [("104", "30")] * 40

    Coordinate(amap).convert(locations)

    assert http.requests[0].params["locations"].count("|") == 39


@pytest.mark.parametrize(
    "locations",
    [
        [],
        [("104", "30")] * 41,
    ],
)
def test_convert_rejects_invalid_location_count(sync_client, locations):
    amap, http = sync_client

    with pytest.raises(ValueError):
        Coordinate(amap).convert(locations)

    assert http.requests == []


@pytest.mark.asyncio
async def test_convert_supports_async_http_client(async_client):
    amap, http = async_client

    result = await Coordinate(amap).convert([("104.07", "30.66")])

    assert result == {"status": "1", "info": "OK"}
    assert http.requests[0].path == "/v3/assistant/coordinate/convert"
