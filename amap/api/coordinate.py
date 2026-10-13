"""
坐标转换
- GPS / 百度 / mapbar → 高德
- 端点: /v3/assistant/coordinate/convert
- 文档:https://lbs.amap.com/api/webservice/guide/api/convert
"""

from collections.abc import Sequence
from typing import Any, Literal

from amap import base
from amap.types import Coordinate as _Coord
from amap.types import T_OutputFormat, format_coordinates

T_CoordSystem = Literal["gps", "mapbar", "baidu", "autonavi"]
"""原坐标系:gps-mapbar-baidu-autonavi(不转换)"""


class Coordinate(base.ApiAgent[base.AmapResultT]):
    """
    坐标转换
    地址:https://lbs.amap.com/api/webservice/guide/api/convert
    """

    def convert(
        self,
        locations: Sequence[_Coord],
        *,
        coordsys: T_CoordSystem = "autonavi",
        sig: str | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """非高德坐标批量转换为高德坐标

        Args:
            locations: 坐标点列表,最多 40 个
            coordsys: 原坐标系
            sig: 数字签名
            output: 返回格式 json/xml
        """
        if not locations:
            raise ValueError("locations should not be empty")
        if len(locations) > 40:
            raise ValueError("locations should not more than 40")

        params: dict[str, Any] = {
            "locations": format_coordinates(locations),
            "coordsys": coordsys,
            "output": output.upper(),
        }
        if sig is not None:
            params["sig"] = sig

        return self.amap.http.get("/v3/assistant/coordinate/convert", params=params)
