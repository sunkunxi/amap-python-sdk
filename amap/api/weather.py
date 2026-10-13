from typing import Any

from amap import base
from amap.types import T_Extensions, T_OutputFormat


class Weather(base.ApiAgent[base.AmapResultT]):
    """
    天气查询
    地址：https://lbs.amap.com/api/webservice/guide/api-advanced/weatherinfo
    """

    def info(
        self,
        city: str,
        *,
        extensions: T_Extensions | None = None,
        output: T_OutputFormat = "json",
    ) -> base.AmapResultT:
        """天气查询"""

        params: dict[str, Any] = {}

        params["city"] = city
        if extensions is not None:
            params["extensions"] = extensions

        if output is not None:
            # NOTE: it is uppercase "JSON" or "XML" in official doc
            params["output"] = output.upper()

        return self.amap.http.get("/v3/weather/weatherInfo", params=params)
