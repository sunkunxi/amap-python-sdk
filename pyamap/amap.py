import logging

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
from pyamap.exceptions import AmapAPIError, AmapTimeoutError

from .types import RequestMethods, T_Headers, T_Params

logger = logging.getLogger(__name__)


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
            res.raise_for_status()
            result = self._validate_response(res.json())
        except requests.exceptions.Timeout as exc:
            logger.warning("Amap request timed out method=%s path=%s", method, path)
            raise AmapTimeoutError("Amap request timed out") from exc
        except requests.exceptions.RequestException as exc:
            logger.warning(
                "Amap HTTP request failed method=%s path=%s error_type=%s",
                method,
                path,
                type(exc).__name__,
            )
            raise
        except AmapAPIError as exc:
            logger.warning(
                "Amap API request failed method=%s path=%s infocode=%s",
                method,
                path,
                exc.infocode,
            )
            raise

        logger.debug(
            "Amap request succeeded method=%s path=%s status_code=%s",
            method,
            path,
            res.status_code,
        )
        return result

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
        logger.debug("Closing synchronous Amap HTTP client")
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
