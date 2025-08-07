import abc
import logging
from urllib.parse import urljoin

from .types import T_Headers, T_Params

logger = logging.getLogger(__name__)


class HTTPClient(metaclass=abc.ABCMeta):
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    @abc.abstractmethod
    def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        raise NotImplementedError()

    @abc.abstractmethod
    def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        raise NotImplementedError()

    @abc.abstractmethod
    def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ):
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()


class Amap(abc.ABC):
    BASE_URL = "https://restapi.amap.com"

    @property
    @abc.abstractmethod
    def http(self) -> HTTPClient:
        raise NotImplementedError()

    def close(self):
        return self.http.close()


class ApiAgent(abc.ABC):
    def __init__(self, amap: Amap):
        self.amap = amap
