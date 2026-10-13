import pytest

from amap.api.place import Place


def test_text_search_serializes_filters_and_page_options(sync_client):
    amap, http = sync_client

    Place(amap).text(
        "咖啡",
        types=["050000", "060000"],
        region="成都",
        city_limit=True,
        show_fields=["business", "photos"],
        page_size=25,
        page_num=2,
        sig="signature",
    )

    assert http.requests[0].path == "/v5/place/text"
    assert http.requests[0].params == {
        "keywords": "咖啡",
        "types": "050000|060000",
        "region": "成都",
        "city_limit": True,
        "show_fields": "business,photos",
        "page_size": 25,
        "page_num": 2,
        "sig": "signature",
        "output": "json",
    }


def test_text_search_accepts_80_character_keyword_and_none_output(sync_client):
    amap, http = sync_client

    Place(amap).text("x" * 80, output=None)

    assert http.requests[0].params == {"keywords": "x" * 80}


def test_internal_param_builder_supports_callback(sync_client):
    amap, _ = sync_client

    params = Place(amap)._init_params(callback=lambda: None)

    assert callable(params["callback"])


@pytest.mark.parametrize(
    "kwargs",
    [
        {"search_term": "x" * 81},
        {"page_size": 0},
        {"page_size": 26},
        {"page_num": 0},
    ],
)
def test_text_search_rejects_invalid_inputs(sync_client, kwargs):
    amap, http = sync_client

    with pytest.raises(ValueError):
        Place(amap).text(kwargs.pop("search_term", "coffee"), **kwargs)

    assert http.requests == []


def test_around_search_formats_location_and_optional_radius(sync_client):
    amap, http = sync_client

    Place(amap).around(
        "咖啡",
        location=("104.07", "30.66"),
        radius=5000,
        sortrule="distance",
        region="成都",
    )

    assert http.requests[0].path == "/v5/place/around"
    assert http.requests[0].params == {
        "keywords": "咖啡",
        "region": "成都",
        "output": "json",
        "location": "104.07,30.66",
        "radius": 5000,
        "sortrule": "distance",
    }


@pytest.mark.parametrize("radius", [-1, 5001])
def test_around_search_rejects_radius_out_of_range(sync_client, radius):
    amap, http = sync_client

    with pytest.raises(ValueError):
        Place(amap).around("coffee", location=("104", "30"), radius=radius)

    assert http.requests == []


def test_polygon_search_formats_ring_and_requires_three_vertices(sync_client):
    amap, http = sync_client

    Place(amap).polygon(
        ("104", "30"),
        ("105", "30"),
        ("105", "31"),
        ("104", "30"),
        keywords="coffee",
    )

    assert http.requests[0].path == "/v5/place/polygon"
    assert http.requests[0].params["polygon"] == "104,30|105,30|105,31|104,30"
    assert http.requests[0].params["keywords"] == "coffee"

    with pytest.raises(ValueError):
        Place(amap).polygon(("104", "30"), ("105", "30"))


def test_detail_search_joins_ids_and_limits_count(sync_client):
    amap, http = sync_client

    Place(amap).detail("B001", "B002", show_fields=["business"])

    assert http.requests[0].path == "/v5/place/detail"
    assert http.requests[0].params == {
        "show_fields": "business",
        "output": "json",
        "id": "B001|B002",
    }

    with pytest.raises(ValueError):
        Place(amap).detail(*(f"B{i}" for i in range(11)))


@pytest.mark.asyncio
async def test_place_endpoints_support_async_http_client(async_client):
    amap, http = async_client

    await Place(amap).text("coffee")
    await Place(amap).around("coffee", location=("104", "30"))
    await Place(amap).polygon(("1", "1"), ("2", "2"), ("3", "3"))
    await Place(amap).detail("B001")

    assert [request.path for request in http.requests] == [
        "/v5/place/text",
        "/v5/place/around",
        "/v5/place/polygon",
        "/v5/place/detail",
    ]
