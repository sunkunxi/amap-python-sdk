# pyamap

[![Test](https://github.com/sunkunxi/pyamap/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/sunkunxi/pyamap/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/sunkunxi/pyamap/branch/main/graph/badge.svg)](https://codecov.io/gh/sunkunxi/pyamap)
[![PyPI version](https://img.shields.io/pypi/v/pyamap?color=%2334D058&label=pypi%20package)](https://pypi.org/project/pyamap/)
![Python versions](https://img.shields.io/pypi/pyversions/pyamap.svg?color=%2334D058)

English | [简体中文](./doc/README.zh.md)

## Overview

This repository is a Python client for the [Amap (Gaode) Web Service APIs](https://lbs.amap.com/api/webservice/summary). It provides a synchronous client and a matching asynchronous client for applications built around asyncio.

See the "Available APIs" section below for a table of the Web APIs wrapped by this SDK.

## Installation

```bash
pip install pyamap
```


## API key

Create a Web Service API key in the [Amap developer console](https://console.amap.com/dev/key/app).

## Synchronous usage

The synchronous client is the recommended starting point. Methods return the parsed Amap JSON response as a dictionary.

```python
import os

from amap import Amap

amap = Amap(os.environ["AMAP_API_KEY"])
try:
    # POI keyword search
    pois = amap.place.text(
        "coffee",
        region="上海",
        city_limit=True,
        page_size=10,
        page_num=1,
    )

    # Nearby search; coordinates are (longitude, latitude)
    nearby = amap.place.around(
        "coffee",
        location=("121.4737", "31.2304"),
        radius=1500,
    )

    # Search within a closed polygon (first and last points match)
    in_area = amap.place.polygon(
        ("116.4074", "39.9042"),
        ("116.4200", "39.9042"),
        ("116.4200", "39.9150"),
        ("116.4074", "39.9042"),
        keywords="museum",
    )

    # Retrieve a POI by its Amap ID
    poi = amap.place.detail("YOUR_POI_ID")

    # Other services
    weather = amap.weather.info("110000")
    districts = amap.district.list("北京市")
    geocode = amap.georegeo.geo("北京市朝阳区阜通东大街6号")
    reverse_geocode = amap.georegeo.regeo(("116.481488", "39.990464"))
    route = amap.direction.driving(
        ("116.481028", "39.989643"),
        ("116.434446", "39.90816"),
    )
finally:
    amap.close()
```

Coordinates are provided as `(longitude, latitude)`. The methods accept endpoint-specific keyword arguments; refer to their docstrings and the corresponding Amap API documentation for the full parameter list.

## Asynchronous usage

`amap.aio.Amap` provides the corresponding asyncio client, implemented with aiohttp. Its service methods mirror the synchronous client.

```python
import asyncio
import os

from amap.aio import Amap


async def main():
    async with Amap(os.environ["AMAP_API_KEY"]) as amap:
        result = await amap.place.text("coffee", region="上海")
        print(result)


asyncio.run(main())
```

## Available APIs

The SDK wraps the following Amap Web APIs:

| API                   | Description                                                          | Client module   |
| --------------------- | -------------------------------------------------------------------- | --------------- |
| Place Search (POI)    | Keyword, nearby, polygon, and detail searches for points of interest | amap.place      |
| Weather               | Current weather and forecasts                                        | amap.weather    |
| District              | Administrative district lookup and listing                           | amap.district   |
| Geocoding             | Forward and reverse geocoding                                        | amap.georegeo   |
| Directions            | Route planning (driving, walking, etc.)                              | amap.direction  |
| Distance              | Distance measurement and matrix queries                              | amap.distance   |
| Coordinate Conversion | Convert between coordinate systems                                   | amap.coordinate |
| Input Tips            | Autocomplete / input suggestion service                              | amap.inputtips  |
| IP Location           | IP-based location lookup                                             | amap.ip         |
| Traffic Status        | Traffic condition and incident queries                               | amap.traffic    |

Service availability, required permissions, and API limits should be checked in the official Amap documentation.

## Errors

If Amap returns a JSON response with `"status": "0"`, the client raises `amap.exceptions.AmapAPIError`. The exception exposes the original response, `info`, and `infocode`:

```python
from amap.exceptions import AmapAPIError

try:
    result = amap.place.text("coffee")
except AmapAPIError as exc:
    print(exc.infocode, exc.info)
    print(exc.response)
```

The SDK preserves Amap's `infocode` instead of guessing its meaning from a numeric prefix. Check the [official Amap error-code reference](https://lbs.amap.com/api/webservice/guide/tools/info) and the documentation for the specific API. When the underlying HTTP library reports a request timeout, the client raises `amap.exceptions.AmpTimeoutError`; other network and HTTP transport errors are raised by `requests` or `aiohttp`.

## Requirements

- Python `>=3.10,<4.0`
- `requests` for the synchronous client
- `aiohttp` for the asynchronous client

Exact dependency constraints are maintained in [pyproject.toml](pyproject.toml).

## Contributing

Contributions are welcome. If submitting changes, please include unit tests for any behavior changes or new features.

Run the test suite with:

```bash
uv run pytest
```

## License

MIT
