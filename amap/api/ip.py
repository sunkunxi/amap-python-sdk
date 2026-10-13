"""
IP 定位
- 端点: /v3/ip
- 文档:https://lbs.amap.com/api/webservice/guide/api/ipconfig
"""

from typing import Any

from amap import base
from amap.types import T_OutputFormat


class Ip(base.ApiAgent[base.AmapResultT]):
    """
    IP 定位
    地址:https://lbs.amap.com/api/webservice/guide/api/ipconfig
    """

    def locate(
        self,
        ip: str | None = None,
        *,
        sig: str | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """根据 IP 定位

        Args:
            ip: IP 地址(仅支持国内,留空则取请求方 IP)
            sig: 数字签名
            output: 返回格式 json/xml
        """
        params: dict[str, Any] = {
            "output": output.upper(),
        }
        if ip is not None:
            params["ip"] = ip
        if sig is not None:
            params["sig"] = sig

        return self.amap.http.get("/v3/ip", params=params)
