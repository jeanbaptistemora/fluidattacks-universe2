# pylint: skip-file

from dataclasses import (
    dataclass,
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


@dataclass(frozen=True)
class RawClient:
    url_base: str
    headers: Dict[str, Any]
    max_retries: int
    handler: Patch[ErrorHandler]

    def try_get(
        self, endpoint: str, params: Dict[str, Any], **kargs: Any
    ) -> RawResponse:
        response = requests.get(
            f"{self.url_base}{endpoint}",
            headers=self.headers,
            params=params,
            **kargs,
        )
        error = _extract_http_error(response)
        if error == Maybe.empty:
            return IOSuccess(response)
        return IOFailure(error.unwrap())

    def get(
        self, endpoint: str, params: Dict[str, Any], **kargs: Any
    ) -> IO[Response]:
        request = lambda: self.try_get(endpoint, params, **kargs)
        return insistent_call(request, self.handler.unwrap, self.max_retries)
