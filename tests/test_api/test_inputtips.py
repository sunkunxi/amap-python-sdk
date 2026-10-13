import pytest

from pyamap.api.inputtips import InputTips


def test_query_uses_keyword_and_default_values(sync_client):
    amap, http = sync_client

    InputTips(amap).query("咖啡")

    assert http.requests[0].path == "/v3/assistant/inputtips"
    assert http.requests[0].params == {
        "keywords": "咖啡",
        "datatype": "all",
        "output": "JSON",
    }


def test_query_serializes_all_optional_fields(sync_client):
    amap, http = sync_client

    InputTips(amap).query(
        "咖啡",
        types="050000|060000",
        location=("104.07", "30.66"),
        city="510100",
        citylimit=True,
        datatype="poi",
        sig="signature",
        output="xml",
    )

    assert http.requests[0].params == {
        "keywords": "咖啡",
        "datatype": "poi",
        "output": "XML",
        "types": "050000|060000",
        "location": "104.07,30.66",
        "city": "510100",
        "citylimit": "true",
        "sig": "signature",
    }


def test_query_accepts_string_citylimit_and_omits_none_fields(sync_client):
    amap, http = sync_client

    InputTips(amap).query("成都", citylimit="false")

    assert http.requests[0].params["citylimit"] == "false"
    assert "city" not in http.requests[0].params
    assert "location" not in http.requests[0].params


@pytest.mark.asyncio
async def test_query_supports_async_http_client(async_client):
    amap, http = async_client

    result = await InputTips(amap).query("成都")

    assert result["status"] == "1"
    assert http.requests[0].path == "/v3/assistant/inputtips"
