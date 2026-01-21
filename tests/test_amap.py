from pyamap.amap import HTTPClient
from pyamap.api.district import District
from pyamap.api.georegeo import Georegeo
from pyamap.api.place import Place
from pyamap.api.weather import Weather


def test_amap_init(amap):
    assert amap


def test_amap_http_client(amap):
    assert amap.http and isinstance(amap.http, HTTPClient)


def test_amap_api_agent(amap):
    assert amap.place and isinstance(amap.place, Place)
    assert amap.weather and isinstance(amap.weather, Weather)
    assert amap.district and isinstance(amap.district, District)
    assert amap.georegeo and isinstance(amap.georegeo, Georegeo)
