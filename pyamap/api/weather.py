from typing import Any, Literal

from pyamap import base


class Weather(base.ApiAgent):
    """
    天气查询
    地址：https://lbs.amap.com/api/webservice/guide/api-advanced/weatherinfo
    """

    def info(
        self,
        city: str,
        *,
        extensions: Literal["base", "all"] | None = None,
        output: Literal["json", "xml"] | None = None,
    ) -> base.AmapResult:
        """天气查询"""

        params: dict[str, Any] = {}

        params["city"] = city
        if extensions is not None:
            params["extensions"] = extensions

        if output is not None:
            # NOTE: it is uppercase "JSON" or "XML" in official doc
            params["extensions"] = output.upper()

        return self.amap.http.get("/v3/weather/weatherInfo", params=params)
