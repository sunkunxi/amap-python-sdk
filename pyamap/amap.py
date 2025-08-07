import requests

from pyamap import base
from pyamap.api.place import Place
from pyamap.api.weather import Weather

from .types import T_Headers, T_Params


class HTTPClient(base.HTTPClient):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        url = self.url(path)
        params["key"] = self.api_key
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
        params["key"] = self.api_key
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
        params["key"] = self.api_key
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
        params["key"] = self.api_key
        return self.session.post(url, params=params, headers=headers)

    def close(self) -> None:
        self.session.close()


class Amap(base.Amap):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

        self.place = Place(self)
        self.weather = Weather(self)

        self._http = HTTPClient(self.api_key, self.BASE_URL)

    @property
    def http(self) -> HTTPClient:
        return self._http
