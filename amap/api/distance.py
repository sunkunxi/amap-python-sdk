"""
距离测量
- 端点: /v3/distance
- 文档:https://lbs.amap.com/api/webservice/guide/api/distance
"""

from collections.abc import Sequence
from typing import Any, Literal

from amap import base
from amap.types import Coordinate, T_OutputFormat, format_coordinate, format_coordinates

T_DistanceType = Literal[0, 1, 2, 3]
"""距离测量类型:
0-直线距离
1-驾车导航距离(仅支持国内坐标对)
2-公交规划距离(仅支持市内,需要起点城市)
3-步行规划距离(仅支持 5km 以内)
"""


class Distance(base.ApiAgent[base.AmapResultT]):
    """
    距离测量
    地址:https://lbs.amap.com/api/webservice/guide/api/distance
    """

    def measure(
        self,
        origins: Sequence[Coordinate],
        destination: Coordinate,
        *,
        type: T_DistanceType = 1,
        sig: str | None = None,
        output: T_OutputFormat = "json",
        callback: str | None = None,
    ) -> base.AmapResultT:
        """测量一个起点到一组终点的距离

        Args:
            origins: 起点坐标列表,最多 100 个
            destination: 终点坐标 (lon, lat),只能一个
            type: 距离测量类型
            sig: 数字签名
            output: 返回格式 json/xml
            callback: JSONP 回调函数名
        """
        if not origins:
            raise ValueError("origins should not be empty")
        if len(origins) > 100:
            raise ValueError("origins should not more than 100")

        params: dict[str, Any] = {
            "origins": format_coordinates(origins),
            "destination": format_coordinate(destination),
            "type": type,
            "output": output.upper(),
        }
        if sig is not None:
            params["sig"] = sig
        if callback is not None:
            params["callback"] = callback

        return self.amap.http.get("/v3/distance", params=params)
