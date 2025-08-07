import os
from decimal import Decimal

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from pyamap import Amap
from pyamap.aio import Amap as AioAmap


@pytest.fixture(scope="session")
def sample_coordinate() -> tuple[Decimal, Decimal]:
    # Chendu
    longitude = Decimal("104.07")
    latitude = Decimal("30.66")

    return longitude, latitude


@pytest.fixture(scope="session")
def sample_polygon() -> list[tuple[Decimal, Decimal]]:
    # Chengdu
    left_top = Decimal("103.95"), Decimal("30.77")
    right_bottom = Decimal("104.16"), Decimal("30.60")

    return [left_top, right_bottom]


@pytest.fixture(scope="session")
def sample_ids() -> list[str]:
    return ["", ""]


@pytest.fixture(scope="session")
def api_key() -> str:
    load_dotenv()
    key = os.getenv("API_KEY")
    if not key:
        raise ValueError("API_KEY Not Found in env variable")
    return key


@pytest.fixture(scope="session")
def amap(api_key: str):
    return Amap(api_key)


@pytest_asyncio.fixture(scope="function")
async def aio_amap(api_key: str):
    async with AioAmap(api_key=api_key) as aio_amap:
        yield aio_amap
