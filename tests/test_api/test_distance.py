import pytest

from amap.api.distance import Distance


def test_measure_serializes_origins_destination_and_defaults(sync_client):
    amap, http = sync_client

    result = Distance(amap).measure(
        origins=[("104.07", "30.66"), ("104.08", "30.67")],
        destination=("104.07", "30.69"),
    )

    assert result["status"] == "1"
    assert http.requests[0].path == "/v3/distance"
    assert http.requests[0].params == {
        "origins": "104.07,30.66|104.08,30.67",
        "destination": "104.07,30.69",
        "type": 1,
        "output": "JSON",
    }


def test_measure_serializes_optional_params(sync_client):
    amap, http = sync_client

    Distance(amap).measure(
        origins=[("104.07", "30.66")],
        destination=("104.07", "30.69"),
        type=0,
        sig="signature",
        output="xml",
        callback="handleResult",
    )

    assert http.requests[0].params == {
        "origins": "104.07,30.66",
        "destination": "104.07,30.69",
        "type": 0,
        "output": "XML",
        "sig": "signature",
        "callback": "handleResult",
    }


@pytest.mark.parametrize("origins", [[], [("104", "30")] * 101])
def test_measure_rejects_empty_or_more_than_100_origins(sync_client, origins):
    amap, http = sync_client

    with pytest.raises(ValueError):
        Distance(amap).measure(origins, ("104", "30"))

    assert http.requests == []


@pytest.mark.asyncio
async def test_measure_supports_async_http_client(async_client):
    amap, http = async_client

    result = await Distance(amap).measure([("104", "30")], ("104", "31"))

    assert result["status"] == "1"
    assert http.requests[0].path == "/v3/distance"
