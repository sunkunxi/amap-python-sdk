from collections.abc import Awaitable

import aiohttp
from typing_extensions import Self

from pyamap import base
from pyamap.api.district import District
from pyamap.api.georegeo import Georegeo
from pyamap.api.place import Place
from pyamap.api.weather import Weather

from .types import RequestMethods, T_Headers, T_Params


class HTTPClient(base.HTTPClient[Awaitable[base.AmapResult]]):
    def __init__(self, *args, max_connector: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.connector = aiohttp.TCPConnector(limit=max_connector)
        self.session = aiohttp.ClientSession(connector=self.connector)

    def _prepara_params(self, params: T_Params) -> T_Params:
        params["key"] = self.api_key

        # convert python bool to "true" or "false"
        return {k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items()}

    async def _request(
        self,
        method: RequestMethods,
        *,
        path: str,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        url = self.url(path)
        params = self._prepara_params(params)
        res = await self.session.request(method, url, params=params, headers=headers, data=data)
        return await res.json()

    async def get(
        self,
        path: str,
        *,
        params: T_Params,
        headers: T_Headers | None = None,
        data: str | None = None,
    ) -> base.AmapResult:
        return await self._request("GET", path=path, params=params, headers=headers, data=data)

    async def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        return await self._request("PUT", path=path, params=params, headers=headers, data=data)

    async def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        return await self._request("DELETE", path=path, params=params, headers=headers, data=data)

    async def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        return await self._request("POST", path=path, params=params, headers=headers, data=data)

    async def close(self) -> None:
        await self.session.close()


class Amap(base.Amap[Awaitable[base.AmapResult]]):
    def __init__(self, api_key: str, max_connector: int = 100) -> None:
        self.api_key = api_key
        self.max_connector = max_connector

        self.place = Place(self)
        self.weather = Weather(self)
        self.district = District(self)
        self.georegeo = Georegeo(self)

        self._http = None

    @property
    def http(self) -> HTTPClient:
        if self._http is None:
            raise RuntimeError(
                "aiohttp client not initialized. Use 'async with Amap(api_key) as amap'"
            )
        return self._http

    async def initialize(self) -> Self:
        self._http = HTTPClient(  # type: ignore[assignment]
            self.api_key,
            self.BASE_URL,
            max_connector=self.max_connector,
        )
        return self

    async def __aenter__(self):
        return await self.initialize()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    def __await__(self):
        return self.initialize().__await__()

    async def close(self):
        return await self.http.close()
