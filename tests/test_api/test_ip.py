import pytest

from pyamap.api.ip import Ip


def test_ip_locate(amap):
    ip = Ip(amap)
    res = ip.locate()
    assert res


def test_ip_locate_with_ip(amap):
    ip = Ip(amap)
    res = ip.locate(ip="114.114.114.114")
    assert res


@pytest.mark.asyncio
async def test_aio_ip_locate(aio_amap):
    ip = Ip(aio_amap)
    res = await ip.locate()
    assert res
