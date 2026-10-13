"""
交通态势(高级服务,需商务开通)
- 圆形区域: /v3/traffic/status/circle
- 矩形区域: /v3/traffic/status/rectangle
- 指定道路: /v3/traffic/status/road
- 文档:https://lbs.amap.com/api/webservice/guide/api-advanced/traffic-situation-inquiry
"""

from typing import Any, Literal

from amap import base
from amap.types import Coordinate, Rectangle, T_OutputFormat, format_coordinate

T_TrafficRoadLevel = Literal[1, 2, 3, 4, 5, 6]
"""道路等级(包含关系):
1-高速
2-城市快速路/国道
3-高速辅路
4-主要道路
5-一般道路(包含 1-4)
6-无名道路(包含 1-5)
"""

T_TrafficExtensions = Literal["base", "all"]
"""返回内容详略:base-基本信息 all-基本+详细(道路列表)"""


class Traffic(base.ApiAgent[base.AmapResultT]):
    """
    交通态势查询
    地址:https://lbs.amap.com/api/webservice/guide/api-advanced/traffic-situation-inquiry

    注意:属于高级服务,需申请,支持城市见官方文档。
    """

    def circle(
        self,
        level: T_TrafficRoadLevel,
        location: Coordinate,
        *,
        radius: int = 1000,
        extensions: T_TrafficExtensions = "base",
        sig: str | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """圆形区域内交通态势

        Args:
            level: 道路等级
            location: 中心点 (lon, lat)
            radius: 半径,单位米,最大 4999,不支持小数
            extensions: base/all
            sig: 数字签名
            output: 返回格式 json/xml
        """
        if not 0 < radius <= 4999:
            raise ValueError("radius should in (0, 4999]")

        params: dict[str, Any] = {
            "level": level,
            "location": format_coordinate(location),
            "radius": radius,
            "extensions": extensions,
            "output": output.upper(),
        }
        if sig is not None:
            params["sig"] = sig

        return self.amap.http.get("/v3/traffic/status/circle", params=params)

    def rectangle(
        self,
        level: T_TrafficRoadLevel,
        rectangle: Rectangle,
        *,
        extensions: T_TrafficExtensions = "base",
        sig: str | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """矩形区域内交通态势

        Args:
            level: 道路等级
            rectangle: 矩形左下右上两个顶点
                ((x1, y1), (x2, y2))
            extensions: base/all
            sig: 数字签名
            output: 返回格式 json/xml
        """
        params: dict[str, Any] = {
            "level": level,
            "rectangle": format_coordinate(rectangle[0]) + ";" + format_coordinate(rectangle[1]),
            "extensions": extensions,
            "output": output.upper(),
        }
        if sig is not None:
            params["sig"] = sig

        return self.amap.http.get("/v3/traffic/status/rectangle", params=params)

    def road(
        self,
        level: T_TrafficRoadLevel,
        name: str,
        *,
        city: str | None = None,
        adcode: str | None = None,
        extensions: T_TrafficExtensions = "base",
        sig: str | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """指定道路交通态势

        Args:
            level: 道路等级
            name: 道路名称
            city: 城市名(不推荐,优先 adcode)
            adcode: 城市 adcode(强烈推荐)
            extensions: base/all
            sig: 数字签名
            output: 返回格式 json/xml
        """
        if city is None and adcode is None:
            raise ValueError("city or adcode is required")

        params: dict[str, Any] = {
            "level": level,
            "name": name,
            "extensions": extensions,
            "output": output.upper(),
        }
        if city is not None:
            params["city"] = city
        if adcode is not None:
            params["adcode"] = adcode
        if sig is not None:
            params["sig"] = sig

        return self.amap.http.get("/v3/traffic/status/road", params=params)
