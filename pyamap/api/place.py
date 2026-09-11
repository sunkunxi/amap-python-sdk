from collections.abc import Callable
from decimal import Decimal
from typing import Any, Literal

from pyamap import base
from pyamap.types import T_ShowFields


class Place(base.ApiAgent):
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
        output: Literal["json"] | None = None,
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
        output: Literal["json"] | None = None,
    ) -> base.AmapResult:
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

    def arround(
        self,
        keywords: str,
        *,
        longitude: str | Decimal,
        latitude: str | Decimal,
        radius: int | None = None,
        types: list[str] | None = None,
        sortrule: Literal["distance", "weight"] | None = None,
        region: str | None = None,
        city_limit: bool | None = None,
        show_fields: T_ShowFields | None = None,
        page_size: int | None = None,
        page_num: int | None = None,
        sig: str | None = None,
        output: Literal["json"] | None = None,
    ) -> base.AmapResult:
        """周边搜索"""

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

        if not longitude or not latitude:
            raise ValueError("longitude and latitude are both required")

        params["location"] = f"{longitude},{latitude}"

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
        *coordinates: tuple[str, str],
        keywords: str | None = None,
        types: list[str] | None = None,
        show_fields: T_ShowFields | None = None,
        page_size: int | None = None,
        page_num: int | None = None,
        sig: str | None = None,
        output: Literal["json"] | None = None,
    ) -> base.AmapResult:
        """多边形区域搜索"""

        params = self._init_params(
            keywords=keywords,
            types=types,
            show_fields=show_fields,
            page_size=page_size,
            page_num=page_num,
            sig=sig,
            output=output,
        )

        if len(coordinates) < 2:
            raise ValueError("at least 2 coordinates")

        params["polygon"] = "|".join(
            [f"{logitude},{latitude}," for logitude, latitude in coordinates]
        )

        return self.amap.http.get("/v5/place/polygon", params=params)

    def detail(
        self,
        *ids: str,
        show_fields: T_ShowFields | None = None,
        sig: str | None = None,
        output: Literal["json"] | None = None,
    ) -> base.AmapResult:
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
