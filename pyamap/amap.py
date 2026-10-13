import requests

from pyamap import base
from pyamap.api.coordinate import Coordinate
from pyamap.api.direction import Direction
from pyamap.api.distance import Distance
from pyamap.api.district import District
from pyamap.api.georegeo import Georegeo
from pyamap.api.inputtips import InputTips
from pyamap.api.ip import Ip
from pyamap.api.place import Place
from pyamap.api.traffic import Traffic
from pyamap.api.weather import Weather
from pyamap.exceptions import AmapTimeoutError

from .types import RequestMethods, T_Headers, T_Params


class HTTPClient(base.HTTPClient[base.AmapResult]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    def _request(
        self,
        method: RequestMethods,
        *,
        path: str,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        url = self.url(path)
        params = self._prepare_params(params)
        try:
            res = self.session.request(method, url, params=params, headers=headers, data=data)
        except requests.exceptions.Timeout as exc:
            raise AmapTimeoutError("Amap request timed out") from exc
        res.raise_for_status()
        return self._validate_response(res.json())

    def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        return self._request("GET", path=path, params=params, data=data, headers=headers)

    def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        return self._request("PUT", path=path, params=params, data=data, headers=headers)

    def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        return self._request("DELETE", path=path, params=params, data=data, headers=headers)

    def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        return self._request("POST", path=path, params=params, data=data, headers=headers)

    def close(self) -> None:
        self.session.close()


class Amap(base.Amap[base.AmapResult]):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

        self.place = Place(self)
        self.weather = Weather(self)
        self.district = District(self)
        self.georegeo = Georegeo(self)
        self.direction = Direction(self)
        self.distance = Distance(self)
        self.coordinate = Coordinate(self)
        self.inputtips = InputTips(self)
        self.ip = Ip(self)
        self.traffic = Traffic(self)

        self._http = HTTPClient(self.api_key, self.BASE_URL)

    @property
    def http(self) -> HTTPClient:
        return self._http
