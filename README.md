# pyamap
高德地图Python SDK

1. web api对接
2. aio支持
3. 类型支持

Example
-------

```python
from pyamap import Amap

amap = Amap("<API_KEY>")

# POI 2.0 API
res = amap.place.text("keywords")
res = amap.place.arround("成都市", longitude="116.407082", latitude="39.910464")
res = amap.place.polygon(("116.407082", "39.910464"), ("117.407082", "40.910464"))
res = amap.place.detail("POI_ID")


# Weather
res = amap.weather.info("成都市")
```
```python

# Aio Example
from pyamap.aio import Amap

amap = Amap("<API_KEY>")

# POI 2.0 API
res = await amap.place.text("keywords")
res = await amap.place.arround("成都市", longitude="116.407082", latitude="39.910464")
res = await amap.place.polygon(("116.407082", "39.910464"), ("117.407082", "40.910464"))
res = await amap.place.detail("POI_ID")


# Weather API
res = amap.weather.info("成都市")
```
