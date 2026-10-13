"""Opt-in end-to-end checks against the real Amap Web API."""

import os

import pytest

from amap.aio import Amap as AsyncAmap
from amap.amap import Amap

pytestmark = pytest.mark.integration

ORIGIN = ("116.397428", "39.90923")
DESTINATION = ("116.407526", "39.908692")
POLYGON = (
    ("116.39", "39.90"),
    ("116.41", "39.90"),
    ("116.41", "39.92"),
    ("116.39", "39.92"),
    ("116.39", "39.90"),
)


@pytest.fixture(scope="module")
def api_key() -> str:
    key = os.environ.get("AMAP_API_KEY")
    if not key:
        pytest.fail("Set AMAP_API_KEY to run live Amap API smoke tests.")
    return key


def assert_api_success(operation: str, response: dict) -> None:
    assert (
        response.get("status") == "1"
    ), f"{operation} failed: info={response.get('info')!r}, infocode={response.get('infocode')!r}"


def test_all_sync_web_api_endpoints(api_key):
    amap = Amap(api_key)
    try:
        responses = {
            "coordinate.convert": amap.coordinate.convert([ORIGIN], coordsys="gps"),
            "direction.walking": amap.direction.walking(ORIGIN, DESTINATION),
            "direction.transit": amap.direction.transit(
                ORIGIN, DESTINATION, city1="010", city2="010"
            ),
            "direction.driving": amap.direction.driving(ORIGIN, DESTINATION),
            "direction.bicycling": amap.direction.bicycling(ORIGIN, DESTINATION),
            "direction.electrobike": amap.direction.electrobike(ORIGIN, DESTINATION),
            "distance.measure": amap.distance.measure([ORIGIN], DESTINATION),
            "district.list": amap.district.list("天安门"),
            "georegeo.geo": amap.georegeo.geo("北京市东城区天安门广场", city="北京"),
            "georegeo.regeo": amap.georegeo.regeo(ORIGIN),
            "inputtips.query": amap.inputtips.query("天安门", city="北京"),
            "ip.locate": amap.ip.locate("114.114.114.114"),
            "place.text": amap.place.text("天安门", region="北京市"),
            "place.around": amap.place.around("天安门", location=ORIGIN, radius=1000),
            "place.polygon": amap.place.polygon(*POLYGON, keywords="天安门"),
            "traffic.circle": amap.traffic.circle(4, ORIGIN, radius=1000),
            "traffic.rectangle": amap.traffic.rectangle(
                4, (("116.39", "39.90"), ("116.41", "39.92"))
            ),
            "traffic.road": amap.traffic.road(4, "长安街", adcode="110000"),
            "weather.info": amap.weather.info("110000"),
        }

        for operation, response in responses.items():
            assert_api_success(operation, response)

        pois = responses["place.text"].get("pois", [])
        assert pois, "place.text succeeded but returned no POIs for the detail smoke test"
        poi_id = pois[0].get("id")
        assert poi_id, "place.text returned a POI without an id"
        assert_api_success("place.detail", amap.place.detail(poi_id))
    finally:
        amap.close()


@pytest.mark.asyncio
async def test_all_async_web_api_endpoints(api_key):
    async with AsyncAmap(api_key) as amap:
        responses = {
            "coordinate.convert": await amap.coordinate.convert([ORIGIN], coordsys="gps"),
            "direction.walking": await amap.direction.walking(ORIGIN, DESTINATION),
            "direction.transit": await amap.direction.transit(
                ORIGIN, DESTINATION, city1="010", city2="010"
            ),
            "direction.driving": await amap.direction.driving(ORIGIN, DESTINATION),
            "direction.bicycling": await amap.direction.bicycling(ORIGIN, DESTINATION),
            "direction.electrobike": await amap.direction.electrobike(ORIGIN, DESTINATION),
            "distance.measure": await amap.distance.measure([ORIGIN], DESTINATION),
            "district.list": await amap.district.list("天安门"),
            "georegeo.geo": await amap.georegeo.geo("北京市东城区天安门广场", city="北京"),
            "georegeo.regeo": await amap.georegeo.regeo(ORIGIN),
            "inputtips.query": await amap.inputtips.query("天安门", city="北京"),
            "ip.locate": await amap.ip.locate("114.114.114.114"),
            "place.text": await amap.place.text("天安门", region="北京市"),
            "place.around": await amap.place.around("天安门", location=ORIGIN, radius=1000),
            "place.polygon": await amap.place.polygon(*POLYGON, keywords="天安门"),
            "traffic.circle": await amap.traffic.circle(4, ORIGIN, radius=1000),
            "traffic.rectangle": await amap.traffic.rectangle(
                4, (("116.39", "39.90"), ("116.41", "39.92"))
            ),
            "traffic.road": await amap.traffic.road(4, "长安街", adcode="110000"),
            "weather.info": await amap.weather.info("110000"),
        }

        for operation, response in responses.items():
            assert_api_success(operation, response)

        pois = responses["place.text"].get("pois", [])
        assert pois, "place.text succeeded but returned no POIs for the detail smoke test"
        poi_id = pois[0].get("id")
        assert poi_id, "place.text returned a POI without an id"
        assert_api_success("place.detail", await amap.place.detail(poi_id))
