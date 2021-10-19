# pylint: skip-file

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from paginator.raw_client.handlers import (
    ErrorHandler,
    insistent_call,
    RawResponse,
)
from paginator.raw_client.patch import (
    Patch,
)
import requests  # type: ignore
from requests.exceptions import (  # type: ignore
    HTTPError,
)
from requests.models import (  # type: ignore
    Response,
)
from returns.io import (
    IO,
    IOFailure,
    IOSuccess,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Any,
    Dict,
)


class ResponseError(HTTPError):
    def __init__(self, error: HTTPError) -> None:
        super().__init__(
            response=error.response,
            request=error.request,
        )

    def __str__(self) -> str:
        return f"{self.response.json()}"


def _extract_http_error(response: Response) -> Maybe[HTTPError]:
    try:
        response.raise_for_status()
        return Maybe.empty
    except HTTPError as error:
        return Maybe.from_value(ResponseError(error))


class RequestMethod(Enum):
    GET = "GET"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass(frozen=True)
class RawClient:
    url_base: str
    headers: Dict[str, Any]
    max_retries: int
    handler: Patch[ErrorHandler]

    def _try_call(
        self,
        method: RequestMethod,
        endpoint: str,
        params: Dict[str, Any],
        **kargs: Any,
    ) -> RawResponse:
        response = requests.request(
            method.value,
            f"{self.url_base}{endpoint}",
            headers=self.headers,
            params=params,
            **kargs,
        )
        error = _extract_http_error(response)
        if error == Maybe.empty:
            return IOSuccess(response)
        return IOFailure(error.unwrap())

    def try_get(
        self, endpoint: str, params: Dict[str, Any], **kargs: Any
    ) -> RawResponse:
        return self._try_call(RequestMethod.GET, endpoint, params, **kargs)

    def try_post(
        self, endpoint: str, json: Dict[str, Any], **kargs: Any
    ) -> RawResponse:
        return self._try_call(
            RequestMethod.POST, endpoint, {}, json=json, **kargs
        )

    def get(
        self, endpoint: str, params: Dict[str, Any], **kargs: Any
    ) -> IO[Response]:
        request = lambda: self.try_get(endpoint, params, **kargs)
        return insistent_call(request, self.handler.unwrap, self.max_retries)

    def post(
        self, endpoint: str, json: Dict[str, Any], **kargs: Any
    ) -> IO[Response]:
        request = lambda: self.try_post(endpoint, json, **kargs)
        return insistent_call(request, self.handler.unwrap, self.max_retries)
