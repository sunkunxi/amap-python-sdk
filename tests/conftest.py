from dataclasses import dataclass

import pytest

from pyamap.types import T_Headers, T_Params

MOCK_RESPONSE = {"status": "1", "info": "OK"}


@dataclass
class Request:
    method: str
    path: str
    params: T_Params
    data: str | None
    headers: T_Headers | None


class RecordingHTTPClient:
    def __init__(self) -> None:
        self.requests: list[Request] = []

    def _record(
        self,
        method: str,
        path: str,
        params: T_Params,
        data: str | None,
        headers: T_Headers | None,
    ) -> dict[str, str]:
        self.requests.append(Request(method, path, dict(params), data, headers))
        return dict(MOCK_RESPONSE)

    def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("GET", path, params, data, headers)

    def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("PUT", path, params, data, headers)

    def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("DELETE", path, params, data, headers)

    def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("POST", path, params, data, headers)


class AsyncRecordingHTTPClient(RecordingHTTPClient):
    async def get(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("GET", path, params, data, headers)

    async def put(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("PUT", path, params, data, headers)

    async def delete(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("DELETE", path, params, data, headers)

    async def post(
        self,
        path: str,
        *,
        params: T_Params,
        data: str | None = None,
        headers: T_Headers | None = None,
    ) -> dict[str, str]:
        return self._record("POST", path, params, data, headers)


class FakeAmap:
    def __init__(self, http: RecordingHTTPClient | AsyncRecordingHTTPClient) -> None:
        self.http = http


@pytest.fixture
def sync_client() -> tuple[FakeAmap, RecordingHTTPClient]:
    http = RecordingHTTPClient()
    return FakeAmap(http), http


@pytest.fixture
def async_client() -> tuple[FakeAmap, AsyncRecordingHTTPClient]:
    http = AsyncRecordingHTTPClient()
    return FakeAmap(http), http
