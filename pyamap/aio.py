from typing import TYPE_CHECKING

import aiohttp
from typing_extensions import Self

from pyamap import base
from pyamap.api.place import Place
from pyamap.api.weather import Weather

from .types import T_Headers, T_Params

if TYPE_CHECKING:
    pass


class HTTPClient(base.HTTPClient):
    def __init__(self, *args, max_connector: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.connector = aiohttp.TCPConnector(limit=max_connector)
        self.session = aiohttp.ClientSession(connector=self.connector)

    def _prepara_params(self, params: T_Params) -> T_Params:
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
    ) -> dict:
        url = self.url(path)
        params = self._prepara_params(params)
        return self.session.get(url, params=params, headers=headers, data=data)

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
        return self.session.put(url, params=params, headers=headers, data=data)

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
        return self.session.delete(url, params=params, headers=headers, data=data)

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
        return self.session.post(url, params=params, headers=headers, data=data)

    async def close(self) -> None:
        await self.session.close()


class Amap(base.Amap):
    def __init__(self, api_key: str, max_connector: int = 100) -> None:
        self.api_key = api_key
        self.max_connector = max_connector

        self.place = Place(self)
        self.weather = Weather(self)

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

    async def close(self):
        return await self.http.close()
