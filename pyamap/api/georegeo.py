from decimal import Decimal
from typing import Any, Literal

from pyamap import base


class Georegeo(base.ApiAgent[base.AmapResultT]):
    """
    地理/逆地理编码 2.0
    地址:https://lbs.amap.com/api/webservice/guide/api/georegeo
    """

    def geo(
        self,
        address: str,
        city: str | None = None,
    ) -> base.AmapResultT:
        """地理编码 API 服务地址

        Args:
            address (str): 规则遵循: 国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、
                大厦, 如: 北京市朝阳区阜通东大街6号.
            city (str | None, optional):可选输入内容包括: 指定城市的中文(如北京)、指定城
                的中文全拼(beijing)、citycode(010)、adcode(110000),不支持县级市.当指定城
                市查询内容为空时,会进行全国范围内的地址转换检索.
                adcode信息可参考城市编码表(https://lbs.amap.com/api/webservice/download)
        """

        params: dict[str, Any] = {}

        params["address"] = address

        if city is not None:
            params["city"] = city

        return self.amap.http.get("/v3/geocode/geo", params=params)

    def regeo(
        self,
        longitude: str | Decimal,
        latitude: str | Decimal,
        *,
        poitype: list[str] | None = None,
        radius: int | None = None,
        extensions: Literal["base", "all"] = "base",
        roadlevel: Literal[0, 1] | None = None,
        homeorcorp: Literal[0, 1, 2] | None = 0,
    ) -> base.AmapResultT:
        """逆地理编码 API 服务地址

        Args:
            longitude (str | Decimal): 经度
            latitude (str | Decimal): 纬度
            poitype (list[str] | None, optional): 返回附近 POI 类型
                以下内容需要 extensions 参数为 all 时才生效.
                逆地理编码在进行坐标解析之后不仅可以返回地址描述,也可以返回经纬度附近符合限定要求的 POI 内容（在 extensions 字段值为 all 时才会返回 POI 内容）.设置 POI 类型参数相当于为上述操作限定要求.参数仅支持传入 POI TYPECODE,可以传入多个 POI TYPECODE,相互之间用“|”分隔.
                取 POI TYPECODE 可以参考 POI 分类码表(https://a.amap.com/lbs/static/amap_3dmap_lite/amap_poicode.zip)
            radius (int | None, optional): radius 取值范围:0~3000,默认值:1000.单位:米
            extensions (Literal["base", "all"], optional): extensions 参数取值为 all 时会返回基本地址信息、附近 POI 内容、道路信息以及道路交叉口信息.
            roadlevel (Literal[0,1] | None, optional): 道路等级.需要 extensions 参数为 all 时才生效.
                0: 显示所有道路
                1  过滤非主干道路,仅输出主干道路数据
            homeorcorp (int): 是否优化 POI 返回顺序,
                以下内容需要 extensions 参数为 all 时才生效.
                homeorcorp 参数的设置可以影响召回 POI 内容的排序策略,目前提供三个可选参数:
                0:不对召回的排序策略进行干扰.
                1:综合大数据分析将居家相关的 POI 内容优先返回,即优化返回结果中 pois 字段的poi 顺序.
                2:综合大数据分析将公司相关的 POI 内容优先返回,即优化返回结果中 pois 字段的poi 顺序.
        """

        params: dict[str, Any] = {}

        params["location"] = f"{longitude},{latitude}"

        if poitype is not None:
            params["poitype"] = poitype

        if radius is not None:
            if radius > 3000 or radius < 0:
                raise ValueError("radius should between [0, 3000]")
            params["radius"] = radius

        params["extensions"] = extensions

        if roadlevel is not None:
            params["roadlevel"] = roadlevel

        if homeorcorp is not None:
            params["homeorcorp"] = homeorcorp

        return self.amap.http.get("/v3/geocode/regeo", params=params)
