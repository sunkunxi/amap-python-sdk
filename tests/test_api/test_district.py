import pytest

from pyamap.api.district import District


def test_list_uses_documented_defaults(sync_client):
    amap, http = sync_client

    District(amap).list()

    assert http.requests[0].path == "/v3/config/district"
    assert http.requests[0].params == {
        "subdistrict": 1,
        "page": 1,
        "offset": 20,
        "extensions": "base",
        "output": "JSON",
    }


def test_list_serializes_keyword_and_all_optional_params(sync_client):
    amap, http = sync_client

    District(amap).list(
        "成都",
        level=0,
        page_num=2,
        page_size=50,
        extensions="all",
        adcode="510100",
        output="xml",
    )

    assert http.requests[0].params == {
        "keywords": "成都",
        "subdistrict": 0,
        "page": 2,
        "offset": 50,
        "extensions": "all",
        "adcode": "510100",
        "output": "XML",
    }


def test_list_omits_explicitly_disabled_optional_params(sync_client):
    amap, http = sync_client

    District(amap).list(
        level=None,
        page_num=None,
        page_size=None,
        extensions=None,
        adcode=None,
        output=None,
    )

    assert http.requests[0].params == {}


@pytest.mark.parametrize(
    "kwargs",
    [
        {"keywords": "x" * 81},
        {"page_num": 0},
        {"page_size": 0},
    ],
)
def test_list_rejects_invalid_values(sync_client, kwargs):
    amap, http = sync_client

    with pytest.raises(ValueError):
        District(amap).list(**kwargs)

    assert http.requests == []


@pytest.mark.asyncio
async def test_list_supports_async_http_client(async_client):
    amap, http = async_client

    result = await District(amap).list(adcode="510100")

    assert result["status"] == "1"
    assert http.requests[0].params["adcode"] == "510100"
