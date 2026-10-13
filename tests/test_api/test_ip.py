import pytest

from pyamap.api.ip import Ip


def test_locate_omits_ip_by_default(sync_client):
    amap, http = sync_client

    Ip(amap).locate()

    assert http.requests[0].path == "/v3/ip"
    assert http.requests[0].params == {"output": "JSON"}


def test_locate_serializes_ip_signature_and_output(sync_client):
    amap, http = sync_client

    Ip(amap).locate("114.114.114.114", sig="signature", output="xml")

    assert http.requests[0].params == {
        "output": "XML",
        "ip": "114.114.114.114",
        "sig": "signature",
    }


@pytest.mark.asyncio
async def test_locate_supports_async_http_client(async_client):
    amap, http = async_client

    result = await Ip(amap).locate("114.114.114.114")

    assert result["status"] == "1"
    assert http.requests[0].params["ip"] == "114.114.114.114"
