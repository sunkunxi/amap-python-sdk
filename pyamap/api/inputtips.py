"""
输入提示(关键字自动补全)
- 端点: /v3/assistant/inputtips
- 文档:https://lbs.amap.com/api/webservice/guide/api-advanced/inputtips
"""

from typing import Any, Literal

from pyamap import base
from pyamap.types import Coordinate, T_OutputFormat, format_coordinate

T_InputTipsDataType = Literal["all", "poi", "bus", "busline"]
"""返回数据类型:all-所有 poi-POI bus-公交站点 busline-公交线路"""

T_InputTipsCityLimit = Literal["true", "false"]
"""是否仅返回指定城市数据(注意:官方使用字符串 "true"/"false")"""


class InputTips(base.ApiAgent[base.AmapResultT]):
    """
    输入提示
    地址:https://lbs.amap.com/api/webservice/guide/api-advanced/inputtips
    """

    def query(
        self,
        keywords: str,
        *,
        types: str | None = None,
        location: Coordinate | None = None,
        city: str | None = None,
        citylimit: T_InputTipsCityLimit | bool | None = None,
        datatype: T_InputTipsDataType = "all",
        sig: str | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """关键字自动补全

        Args:
            keywords: 查询关键词(必填)
            types: 查询 POI 类型,多个用 "|" 分隔
            location: 附近优先 (lon, lat)
            city: 城市限定,citycode 或 adcode
            citylimit: 仅返回指定城市数据。
                注意官方使用字符串 "true"/"false",这里兼容 bool
            datatype: 返回数据类型
            sig: 数字签名
            output: 返回格式 json/xml
        """
        params: dict[str, Any] = {
            "keywords": keywords,
            "datatype": datatype,
            "output": output.upper(),
        }
        if types is not None:
            params["types"] = types
        if location is not None:
            params["location"] = format_coordinate(location)
        if city is not None:
            params["city"] = city
        if citylimit is not None:
            # 官方使用字符串 "true"/"false",非 JSON 布尔
            params["citylimit"] = (
                str(citylimit).lower() if isinstance(citylimit, bool) else citylimit
            )
        if sig is not None:
            params["sig"] = sig

        return self.amap.http.get("/v3/assistant/inputtips", params=params)
