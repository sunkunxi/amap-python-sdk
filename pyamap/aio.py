from typing import TYPE_CHECKING

import aiohttp

from pyamap import base
from pyamap.api.place import Place
from pyamap.api.weather import Weather

from .types import T_Headers, T_Params

if TYPE_CHECKING:
    from types import TracebackType


class HTTPClient(base.HTTPClient):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.session = aiohttp.ClientSession()

    def _prepara_params(self, params: T_Params):
        params["key"] = self.api_key

        # convert python bool to "true" or "false"
        return {k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items()}

    def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        url = self.url(path)
        params = self._prepara_params(params)
        return self.session.get(url, params=params, headers=headers)

    def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        url = self.url(path)
        params = self._prepara_params(params)
        return self.session.put(url, params=params, headers=headers)

    def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        url = self.url(path)
        params = self._prepara_params(params)
        return self.session.delete(url, params=params, headers=headers)

    def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        url = self.url(path)
        params = self._prepara_params(params)
        return self.session.post(url, params=params, headers=headers)

    async def close(self) -> None:
        await self.session.close()


class Amap(base.Amap):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

        self.place = Place(self)
        self.weather = Weather(self)

        self._http = None

    @property
    def http(self) -> HTTPClient:
        if self._http is None:
            self._http = HTTPClient(self.api_key, self.BASE_URL)  # type:ignore[assignment]
        return self._http  # type: ignore[return-value]

    async def close(self):
        return await self.http.close()
