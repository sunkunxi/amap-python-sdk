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

from .types import T_Headers, T_Params


class HTTPClient(base.HTTPClient[base.AmapResult]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    def _prepare_params(self, params: T_Params) -> T_Params:
        params["key"] = self.api_key
        return {k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items()}

    def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        url = self.url(path)
        params = self._prepare_params(params)
        res = self.session.get(url, params=params, headers=headers, data=data)
        return res.json()

    def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        url = self.url(path)
        params = self._prepare_params(params)
        res = self.session.put(url, params=params, headers=headers, data=data)
        return res.json()

    def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        url = self.url(path)
        params = self._prepare_params(params)
        res = self.session.delete(url, params=params, headers=headers, data=data)
        return res.json()

    def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> base.AmapResult:
        url = self.url(path)
        params = self._prepare_params(params)
        res = self.session.post(url, params=params, headers=headers, data=data)
        return res.json()

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
