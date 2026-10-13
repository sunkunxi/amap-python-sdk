# amap-python-sdk

[![Test](https://github.com/sunkunxi/amap-python-sdk/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/sunkunxi/amap-python-sdk/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/sunkunxi/amap-python-sdk/branch/main/graph/badge.svg)](https://codecov.io/gh/sunkunxi/amap-python-sdk)
[![PyPI version](https://img.shields.io/pypi/v/amap-python-sdk)](https://pypi.org/project/amap-python-sdk/)
![Python versions](https://img.shields.io/badge/python-3.10%2B-blue.svg)

English | [简体中文](./doc/README.zh.md)

## Overview

amap is a Python client for the [Amap (Gaode) Web Service APIs](https://lbs.amap.com/api/webservice/summary). It provides a synchronous client for everyday use and a matching asynchronous client for applications built around asyncio.

The SDK currently wraps Place Search, Weather, District, Geocoding, Directions, Distance, Coordinate Conversion, Input Tips, IP Location, and Traffic Status APIs. Check the linked Amap documentation for service availability, required permissions, and current API limits.

## Installation

```bash
pip install amap-python-sdk
```

The PyPI distribution is named `amap-python-sdk`; the Python import package remains `amap`. The package supports Python 3.10 and later, and installs its HTTP dependencies (`requests` and `aiohttp`) automatically.

## API key

Create a Web Service API key in the [Amap developer console](https://console.amap.com/dev/key/app). Keep it out of source control. For example, set an environment variable before running your application:

```bash
export AMAP_API_KEY="your-api-key"
```

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

## Logging

amap uses Python's standard `logging` module and does not configure handlers or log levels for your application. Successful requests are logged at `DEBUG`; API, HTTP, and timeout failures are logged at `WARNING`. Log messages include the endpoint and diagnostic status, but omit API keys, request parameters, and response bodies.

Configure logging in your application when needed:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## Requirements

- Python `>=3.10,<4.0`
- `requests` for the synchronous client
- `aiohttp` for the asynchronous client

Exact dependency constraints are maintained in [pyproject.toml](pyproject.toml).

## Contributing

Contributions are welcome:

1. Fork the repository and create a branch for your change.
2. Install the project and development groups with `uv sync --all-groups`.
3. Run the relevant tests with `uv run pytest`.
4. Open a pull request with a concise description of the change.

Please add or update tests for behavior changes and follow the existing formatting and typing conventions.

## Releases

Publishing a GitHub Release builds and tests the package, then publishes it to PyPI using Trusted Publishing. Configure a PyPI Trusted Publisher for project `amap-python-sdk`, repository owner `sunkunxi`, repository `amap-python-sdk`, workflow filename `publish.yml`, and GitHub environment `pypi`.

## License

MIT
