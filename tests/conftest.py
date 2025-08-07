import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from pyamap import Amap
from pyamap.aio import Amap as AioAmap


@pytest.fixture(scope="package")
def api_key() -> str:
    load_dotenv()
    key = os.getenv("API_KEY")
    if not key:
        raise ValueError("API_KEY Not Found")
    return key


@pytest.fixture(scope="function")
def amap(api_key: str):
    return Amap(api_key)


@pytest_asyncio.fixture(scope="function")
async def aio_amap(api_key: str):
    try:
        aio_amap = AioAmap(api_key)
        yield aio_amap
    finally:
        await aio_amap.close()
