# pyamap
高德地图Python SDK

<!--
[![PyPI version](https://img.shields.io/pypi/v/pyamap)](https://pypi.org/project/pyamap/)
-->
[![Test](https://github.com/sunkunxi/pyamap/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/sunkunxi/pyamap/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/sunkunxi/pyamap/branch/main/graph/badge.svg)](https://codecov.io/gh/sunkunxi/pyamap)
![Python versions](https://img.shields.io/badge/python-3.10%2B-blue.svg)

1. web api对接
2. aio支持
3. 类型支持

The code structure of this repository is inspired by [py-consul](!https://github.com/criteo/py-consul)


Example
-------

```python
from pyamap import Amap

amap = Amap("<API_KEY>")

# POI 2.0 API
res = amap.place.text("keywords")
res = amap.place.around("成都市", location=("116.407082", "39.910464"))
res = amap.place.polygon(
    ("116.407082", "39.910464"),
    ("117.407082", "40.910464"),
    ("116.407082", "39.910464"),  # 闭合多边形首尾相同
)
res = amap.place.detail("POI_ID")

# Weather
res = amap.weather.info("成都市")

# District
res = amap.district.list()

```
```python

# Aio Example
from pyamap.aio import Amap

amap = Amap("<API_KEY>")

# POI 2.0 API
res = await amap.place.text("keywords")
res = await amap.place.around("成都市", location=("116.407082", "39.910464"))
res = await amap.place.polygon(
    ("116.407082", "39.910464"),
    ("117.407082", "40.910464"),
    ("116.407082", "39.910464"),
)
res = await amap.place.detail("POI_ID")

# Weather API
res = await amap.weather.info("成都市")

# District
res = await amap.district.list()
```

## 已封装 API

| Api | 方法 | 高德端点 |
|-------|------|----------|
| `place` | `text` / `around` / `polygon` / `detail` | `/v5/place/*` |
| `weather` | `info` | `/v3/weather/weatherInfo` |
| `district` | `list` | `/v3/config/district` |
| `georegeo` | `geo` / `regeo` | `/v3/geocode/*` |
| `direction` | `walking` / `transit` / `driving` / `bicycling` / `electrobike` | `/v5/direction/*` (路径规划 2.0) |
| `distance` | `measure` | `/v3/distance` |
| `coordinate` | `convert` | `/v3/assistant/coordinate/convert` |
| `inputtips` | `query` | `/v3/assistant/inputtips` |
| `ip` | `locate` | `/v3/ip` |
| `traffic` | `circle` / `rectangle` / `road` | `/v3/traffic/status/*` |
