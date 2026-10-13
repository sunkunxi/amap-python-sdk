from pyamap import Amap
from pyamap.aio import Amap as AioAmap


def test_sync_client_initializes_without_network_access():
    amap = Amap("test-key")

    assert amap.http.url("/v3/weather/weatherInfo") == (
        "https://restapi.amap.com/v3/weather/weatherInfo"
    )
    amap.close()


def test_async_client_exposes_api_agents_without_network_access():
    amap = AioAmap("test-key")

    assert amap.place is not None
    assert amap.weather is not None
    assert amap.district is not None
    assert amap.georegeo is not None
    assert amap.max_connector == 100
