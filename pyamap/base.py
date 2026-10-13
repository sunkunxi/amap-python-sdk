import abc
from typing import Any, Generic, TypeVar
from urllib.parse import urljoin

from .exceptions import AmapAPIError
from .types import T_Headers, T_Params

AmapResult = dict[str, Any]
AmapResultT = TypeVar("AmapResultT")


class HTTPClient(Generic[AmapResultT], metaclass=abc.ABCMeta):
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def _prepare_params(self, params: T_Params) -> T_Params:
        prepared = {
            name: str(value).lower() if isinstance(value, bool) else value
            for name, value in params.items()
        }
        prepared["key"] = self.api_key
        return prepared

    @staticmethod
    def _validate_response(result: AmapResult) -> AmapResult:
        if str(result.get("status")) == "0":
            raise AmapAPIError(result)
        return result

    @abc.abstractmethod
    def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> AmapResultT:
        raise NotImplementedError()

    @abc.abstractmethod
    def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> AmapResultT:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> AmapResultT:
        raise NotImplementedError()

    @abc.abstractmethod
    def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> AmapResultT:
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()


class Amap(Generic[AmapResultT], abc.ABC):
    BASE_URL = "https://restapi.amap.com"

    @property
    @abc.abstractmethod
    def http(self) -> HTTPClient[AmapResultT]:
        raise NotImplementedError()

    def close(self):
        return self.http.close()


class ApiAgent(Generic[AmapResultT], abc.ABC):
    def __init__(self, amap: Amap[AmapResultT]):
        self.amap = amap
