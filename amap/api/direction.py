"""
路径规划 2.0 (v5)
- 步行:   /v5/direction/walking
- 公交:   /v5/direction/transit/integrated
- 驾车:   /v5/direction/driving
- 骑行:   /v5/direction/bicycling
- 电动车: /v5/direction/electrobike

文档:https://lbs.amap.com/api/webservice/guide/api/newroute
"""

from collections.abc import Sequence
from typing import Any, Literal

from amap import base
from amap.types import Coordinate, T_OutputFormatV5, format_coordinate, format_coordinates

# ---------------------------------------------------------------- #
# 公共 show_fields 字面量
# ---------------------------------------------------------------- #
T_DrivingShowFields = list[Literal["cost", "tmcs", "navi", "cities", "polyline"]]
"""驾车返回结果控制:cost-费用耗时 tmcs-实时路况 navi-导航动作 cities-途径城市 polyline-路段坐标"""

T_WalkingShowFields = list[Literal["cost", "navi", "polyline"]]
"""步行返回结果控制:cost-费用耗时(含打车) navi-导航动作 polyline-路段坐标"""

T_BicyclingShowFields = list[Literal["cost", "navi", "polyline"]]
"""骑行/电动车返回结果控制"""

T_TransitShowFields = list[Literal["cost", "navi", "polyline"]]
"""公交返回结果控制"""

# ---------------------------------------------------------------- #
# 公交策略
# ---------------------------------------------------------------- #
T_TransitStrategy = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
"""公交换乘策略:
0-推荐模式(默认) 1-最经济 2-最少换乘 3-最少步行
4-最舒适 5-不乘地铁 6-地铁图(需 originpoi+destinationpoi)
7-地铁优先 8-时间短
"""

# ---------------------------------------------------------------- #
# 驾车策略
# ---------------------------------------------------------------- #
T_DrivingStrategy = Literal[
    0,
    1,
    2,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
]
"""驾车算路策略:
单条(只返回一条):0-速度优先 1-费用优先 2-常规最快
多条(返回备选):32-默认/高德推荐 33-躲避拥堵 34-高速优先 35-不走高速
36-少收费 37-大路优先 38-速度最快
39-躲避拥堵+高速优先 40-躲避拥堵+不走高速 41-躲避拥堵+少收费
42-少收费+不走高速 43-躲避拥堵+少收费+不走高速
44-躲避拥堵+大路优先 45-躲避拥堵+速度最快
"""

# ---------------------------------------------------------------- #
# 车辆类型
# ---------------------------------------------------------------- #
T_CarType = Literal[0, 1, 2]
"""车辆类型:0-普通燃油 1-纯电动 2-插电式混动"""

# ---------------------------------------------------------------- #
# 备选路线条数
# ---------------------------------------------------------------- #
T_AlternativeRoute = Literal[1, 2, 3]
"""返回备选路线条数:1-第一条 2-前两条 3-三条(步行/骑行/电动车)"""

T_TransitAlternative = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
"""公交返回方案条数:1-10"""


class Direction(base.ApiAgent[base.AmapResultT]):
    """
    路径规划 2.0 (v5)
    地址:https://lbs.amap.com/api/webservice/guide/api/newroute
    """

    # ------------------------------------------------------------------ #
    # 步行
    # ------------------------------------------------------------------ #
    def walking(
        self,
        origin: Coordinate,
        destination: Coordinate,
        *,
        origin_id: str | None = None,
        destination_id: str | None = None,
        alternative_route: T_AlternativeRoute | None = None,
        show_fields: T_WalkingShowFields | None = None,
        isindoor: Literal[0, 1] = 0,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
        callback: str | None = None,
    ) -> base.AmapResultT:
        """步行路径规划

        Args:
            origin: 起点 (lon, lat)
            destination: 终点 (lon, lat)
            origin_id: 起点 POI ID
            destination_id: 终点 POI ID
            alternative_route: 返回备选路线条数 1/2/3
            show_fields: 返回字段筛选 cost/navi/polyline
            isindoor: 是否需要室内算路 0-否 1-是
            sig: 数字签名
            output: 返回格式,只支持 json
            callback: JSONP 回调函数名
        """
        params: dict[str, Any] = {
            "origin": format_coordinate(origin),
            "destination": format_coordinate(destination),
            "isindoor": isindoor,
            "output": output.upper(),
        }
        if origin_id is not None:
            params["origin_id"] = origin_id
        if destination_id is not None:
            params["destination_id"] = destination_id
        if alternative_route is not None:
            params["alternative_route"] = alternative_route
        if show_fields is not None:
            params["show_fields"] = ",".join(show_fields)
        if sig is not None:
            params["sig"] = sig
        if callback is not None:
            params["callback"] = callback

        return self.amap.http.get("/v5/direction/walking", params=params)

    # ------------------------------------------------------------------ #
    # 公交
    # ------------------------------------------------------------------ #
    def transit(
        self,
        origin: Coordinate,
        destination: Coordinate,
        city1: str,
        *,
        city2: str | None = None,
        originpoi: str | None = None,
        destinationpoi: str | None = None,
        ad1: str | None = None,
        ad2: str | None = None,
        strategy: T_TransitStrategy | None = None,
        alternative_route: T_TransitAlternative | None = None,
        nightflag: Literal[0, 1] | None = None,
        date: str | None = None,
        time: str | None = None,
        show_fields: T_TransitShowFields | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
        callback: str | None = None,
    ) -> base.AmapResultT:
        """公交路径规划

        Args:
            origin: 起点 (lon, lat)
            destination: 终点 (lon, lat)
            city1: 起点城市 citycode(必填)
            city2: 终点城市 citycode(跨城必填)
            originpoi: 起点 POI ID(与 origin 同时填时,优先使用 originpoi)
            destinationpoi: 终点 POI ID
            ad1: 起点行政区 adcode
            ad2: 终点行政区 adcode
            strategy: 公交换乘策略
            alternative_route: 返回方案条数 1-10
            nightflag: 是否考虑夜班车 0/1
            date: 请求日期 2013-10-28
            time: 请求时间 9-54
            show_fields: 返回字段筛选 cost/navi/polyline
            sig: 数字签名
            output: 返回格式,只支持 json
            callback: JSONP 回调函数名
        """
        params: dict[str, Any] = {
            "origin": format_coordinate(origin),
            "destination": format_coordinate(destination),
            "city1": city1,
            "output": output.upper(),
        }
        if city2 is not None:
            params["city2"] = city2
        if originpoi is not None:
            params["originpoi"] = originpoi
        if destinationpoi is not None:
            params["destinationpoi"] = destinationpoi
        if ad1 is not None:
            params["ad1"] = ad1
        if ad2 is not None:
            params["ad2"] = ad2
        if strategy is not None:
            params["strategy"] = strategy
        if alternative_route is not None:
            params["AlternativeRoute"] = alternative_route
        if nightflag is not None:
            params["nightflag"] = nightflag
        if date is not None:
            params["date"] = date
        if time is not None:
            params["time"] = time
        if show_fields is not None:
            params["show_fields"] = ",".join(show_fields)
        if sig is not None:
            params["sig"] = sig
        if callback is not None:
            params["callback"] = callback

        return self.amap.http.get("/v5/direction/transit/integrated", params=params)

    # ------------------------------------------------------------------ #
    # 驾车
    # ------------------------------------------------------------------ #
    def driving(
        self,
        origin: Coordinate,
        destination: Coordinate,
        *,
        destination_type: str | None = None,
        origin_id: str | None = None,
        destination_id: str | None = None,
        strategy: T_DrivingStrategy | None = None,
        waypoints: Sequence[Coordinate] | None = None,
        avoidpolygons: Sequence[Sequence[Coordinate]] | None = None,
        plate: str | None = None,
        cartype: T_CarType | None = None,
        ferry: Literal[0, 1] | None = None,
        show_fields: T_DrivingShowFields | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
        callback: str | None = None,
    ) -> base.AmapResultT:
        """驾车路径规划

        Args:
            origin: 起点 (lon, lat)
            destination: 终点 (lon, lat)
            destination_type: 终点 POI 类别
            origin_id: 起点 POI ID
            destination_id: 终点 POI ID
            strategy: 驾车算路策略(0-2 单条,32-45 多条)
            waypoints: 途经点列表,最多 16 个
            avoidpolygons: 避让区域,最多 32 个,每个多边形最多 16 个顶点
                内部用 ';' 分隔顶点、'|' 分隔多边形
            plate: 车牌号(支持 6 位传统车牌和 7 位新能源车牌),如 "京AHA322"
            cartype: 车辆类型
            ferry: 是否使用轮渡 0-使用 1-不使用
            show_fields: 返回字段筛选 cost/tmcs/navi/cities/polyline
            sig: 数字签名
            output: 返回格式,只支持 json
            callback: JSONP 回调函数名
        """
        params: dict[str, Any] = {
            "origin": format_coordinate(origin),
            "destination": format_coordinate(destination),
            "output": output.upper(),
        }
        if destination_type is not None:
            params["destination_type"] = destination_type
        if origin_id is not None:
            params["origin_id"] = origin_id
        if destination_id is not None:
            params["destination_id"] = destination_id
        if strategy is not None:
            params["strategy"] = strategy
        if waypoints is not None:
            if len(waypoints) > 16:
                raise ValueError("waypoints should not more than 16")
            params["waypoints"] = format_coordinates(waypoints, sep=";")
        if avoidpolygons is not None:
            if len(avoidpolygons) > 32:
                raise ValueError("avoidpolygons should not more than 32")
            params["avoidpolygons"] = "|".join(
                format_coordinates(polygon, sep=";") for polygon in avoidpolygons
            )
        if plate is not None:
            params["plate"] = plate
        if cartype is not None:
            params["cartype"] = cartype
        if ferry is not None:
            params["ferry"] = ferry
        if show_fields is not None:
            params["show_fields"] = ",".join(show_fields)
        if sig is not None:
            params["sig"] = sig
        if callback is not None:
            params["callback"] = callback

        return self.amap.http.get("/v5/direction/driving", params=params)

    # ------------------------------------------------------------------ #
    # 骑行
    # ------------------------------------------------------------------ #
    def bicycling(
        self,
        origin: Coordinate,
        destination: Coordinate,
        *,
        alternative_route: T_AlternativeRoute | None = None,
        show_fields: T_BicyclingShowFields | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
        callback: str | None = None,
    ) -> base.AmapResultT:
        """骑行路径规划

        Args:
            origin: 起点 (lon, lat)
            destination: 终点 (lon, lat)
            alternative_route: 返回备选路线条数 1/2/3
            show_fields: 返回字段筛选 cost/navi/polyline
            sig: 数字签名
            output: 返回格式,只支持 json
            callback: JSONP 回调函数名
        """
        params: dict[str, Any] = {
            "origin": format_coordinate(origin),
            "destination": format_coordinate(destination),
            "output": output.upper(),
        }
        if alternative_route is not None:
            params["alternative_route"] = alternative_route
        if show_fields is not None:
            params["show_fields"] = ",".join(show_fields)
        if sig is not None:
            params["sig"] = sig
        if callback is not None:
            params["callback"] = callback

        return self.amap.http.get("/v5/direction/bicycling", params=params)

    # ------------------------------------------------------------------ #
    # 电动车 (v5 新增)
    # ------------------------------------------------------------------ #
    def electrobike(
        self,
        origin: Coordinate,
        destination: Coordinate,
        *,
        alternative_route: T_AlternativeRoute | None = None,
        show_fields: T_BicyclingShowFields | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
        callback: str | None = None,
    ) -> base.AmapResultT:
        """电动车路径规划(与骑行类似,但会考虑限行)

        Args:
            origin: 起点 (lon, lat)
            destination: 终点 (lon, lat)
            alternative_route: 返回备选路线条数 1/2/3
            show_fields: 返回字段筛选 cost/navi/polyline
            sig: 数字签名
            output: 返回格式,只支持 json
            callback: JSONP 回调函数名
        """
        params: dict[str, Any] = {
            "origin": format_coordinate(origin),
            "destination": format_coordinate(destination),
            "output": output.upper(),
        }
        if alternative_route is not None:
            params["alternative_route"] = alternative_route
        if show_fields is not None:
            params["show_fields"] = ",".join(show_fields)
        if sig is not None:
            params["sig"] = sig
        if callback is not None:
            params["callback"] = callback

        return self.amap.http.get("/v5/direction/electrobike", params=params)
