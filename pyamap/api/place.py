from collections.abc import Callable
from typing import Any, Literal

from pyamap import base
from pyamap.types import Coordinate, T_OutputFormatV5, T_ShowFields, format_coordinates


class Place(base.ApiAgent[base.AmapResultT]):
    """
    POI 2.0
    地址：https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch
    """

    def _init_params(
        self,
        keywords: str | None = None,
        types: list[str] | None = None,
        region: str | None = None,
        city_limit: bool | None = None,
        show_fields: T_ShowFields | None = None,
        page_size: int | None = None,
        page_num: int | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
        callback: Callable | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}

        if keywords is not None:
            if len(keywords) > 80:
                raise ValueError("keywords should no more then 80 characters")

            params["keywords"] = keywords

        if types is not None:
            params["types"] = "|".join(types)

        if region is not None:
            params["region"] = region

        if city_limit is not None:
            params["city_limit"] = city_limit

        if show_fields is not None:
            params["show_fields"] = ",".join(show_fields)

        if page_size is not None:
            if not 1 <= page_size <= 25:
                raise ValueError("page_size show between [1, 25]")
            params["page_size"] = page_size

        if page_num is not None:
            if not page_num >= 1:
                raise ValueError("page_num show larger then 1")
            params["page_num"] = page_num

        if sig is not None:
            params["sig"] = sig

        if output is not None:
            params["output"] = output

        if callback is not None:
            params["callback"] = callback

        return params

    def text(
        self,
        keywords: str,
        *,
        types: list[str] | None = None,
        region: str | None = None,
        city_limit: bool | None = None,
        show_fields: T_ShowFields | None = None,
        page_size: int | None = None,
        page_num: int | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
    ) -> base.AmapResultT:
        """关键字搜索"""

        params = self._init_params(
            keywords=keywords,
            types=types,
            region=region,
            city_limit=city_limit,
            show_fields=show_fields,
            page_size=page_size,
            page_num=page_num,
            sig=sig,
            output=output,
        )

        return self.amap.http.get(path="/v5/place/text", params=params)

    def around(
        self,
        keywords: str,
        *,
        location: Coordinate,
        radius: int | None = None,
        types: list[str] | None = None,
        sortrule: Literal["distance", "weight"] | None = None,
        region: str | None = None,
        city_limit: bool | None = None,
        show_fields: T_ShowFields | None = None,
        page_size: int | None = None,
        page_num: int | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
    ) -> base.AmapResultT:
        """周边搜索

        Args:
            keywords: 搜索关键词
            location: 中心点 (lon, lat),小数点后最多 6 位
            radius: 搜索半径,0~5000 米
            ...
        """

        params = self._init_params(
            keywords=keywords,
            types=types,
            region=region,
            city_limit=city_limit,
            show_fields=show_fields,
            page_size=page_size,
            page_num=page_num,
            sig=sig,
            output=output,
        )

        params["location"] = format_coordinates([location])

        if region is not None:
            params["region"] = region

        if radius is not None:
            if radius > 5000 or radius < 0:
                raise ValueError("radius should between [0, 5000]")
            params["radius"] = radius

        if sortrule is not None:
            params["sortrule"] = sortrule

        return self.amap.http.get("/v5/place/around", params=params)

    def polygon(
        self,
        *coordinates: Coordinate,
        keywords: str | None = None,
        types: list[str] | None = None,
        show_fields: T_ShowFields | None = None,
        page_size: int | None = None,
        page_num: int | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
    ) -> base.AmapResultT:
        """多边形区域搜索

        Args:
            *coordinates: 顶点坐标,至少 3 个,首尾坐标对需相同(闭合多边形)
            keywords: 搜索关键词
            types: POI 类型
        """

        if len(coordinates) < 3:
            raise ValueError("at least 3 coordinates for polygon (closed ring)")

        params = self._init_params(
            keywords=keywords,
            types=types,
            show_fields=show_fields,
            page_size=page_size,
            page_num=page_num,
            sig=sig,
            output=output,
        )

        params["polygon"] = format_coordinates(coordinates, sep="|")

        return self.amap.http.get("/v5/place/polygon", params=params)

    def detail(
        self,
        *ids: str,
        show_fields: T_ShowFields | None = None,
        sig: str | None = None,
        output: T_OutputFormatV5 = "json",
    ) -> base.AmapResultT:
        """ID搜索"""

        params = self._init_params(
            show_fields=show_fields,
            sig=sig,
            output=output,
        )
        if len(ids) > 10:
            raise ValueError("ids should not more then 10")

        params["id"] = "|".join(ids)

        return self.amap.http.get("/v5/place/detail", params=params)
