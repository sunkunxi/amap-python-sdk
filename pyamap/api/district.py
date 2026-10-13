from typing import Any

from pyamap import base
from pyamap.types import T_Extensions, T_OutputFormat


class District(base.ApiAgent[base.AmapResultT]):
    """
    行政区域查询是一类简单的 HTTP 接口，根据用户输入的搜索条件可以帮助用户快速的查找特定的行政区域信息。

    例如: 中国>山东省>济南市>历下区>舜华路街道（国>省>市>区>街道）。

    地址: https://lbs.amap.com/api/webservice/guide/api/district
    """

    def list(
        self,
        keywords: str | None = None,
        *,
        level: int = 1,
        page_num: int = 1,
        page_size: int = 20,
        extensions: T_Extensions = "base",
        adcode: str | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """列出行政区域

        Args:
            keywords (str): 查询关键字
            level (int | None, optional): 展示的层数子级行政区，0-不返回下级行政区，1-返回1级下级行政区，以此类推
            page_num (int | None, optional): 需要第几页数据
            page_size (int | None, optional): 最外层返回数据个数
            extensions (T_Extensions | None, optional): 返回结果控制. base-基础，all-全部
            adcode (str | None, optional): 根据区划过滤
            output (Literal[json, xml] | None, optional): 返回数据格式类型
        """

        params: dict[str, Any] = {}

        if keywords is not None:
            if len(keywords) > 80:
                raise ValueError("keywords should no more then 80 characters")

            params["keywords"] = keywords

        if level is not None:
            params["subdistrict"] = level

        if page_num is not None:
            if not page_num >= 1:
                raise ValueError("page_num show greater then 1")
            params["page"] = page_num

        if page_size is not None:
            if not page_size >= 1:
                raise ValueError("page_size show greater then 1")
            params["offset"] = page_size

        if extensions is not None:
            params["extensions"] = extensions

        if adcode is not None:
            params["adcode"] = extensions

        if output is not None:
            params["output"] = output.upper()

        return self.amap.http.get("/v3/config/district", params=params)
