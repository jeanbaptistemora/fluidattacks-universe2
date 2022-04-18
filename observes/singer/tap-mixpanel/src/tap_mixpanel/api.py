from contextlib import (
    contextmanager,
)
from functools import (
    partial,
)
from ratelimiter import (
    RateLimiter,
)
import requests  # type: ignore
import tempfile
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict,
    IO,
    Iterator,
    NamedTuple,
    Tuple,
)

JSON = Dict[str, Any]
API_BASE_URL = "https://data.mixpanel.com/api/2.0"
rate_limiter = RateLimiter(max_calls=40, period=3600)


class Credentials(NamedTuple):
    api_secret: str
    token: str

    @classmethod
    def from_json(cls, creds: JSON) -> "Credentials":
        return Credentials(
            api_secret=creds["API_secret"], token=creds["token"]
        )


def _export(auth: Tuple[str, str], params: JSON) -> Any:
    with rate_limiter:
        return requests.get(
            f"{API_BASE_URL}/export/", auth=auth, params=params
        )


def _load_data(
    creds: Credentials, event: str, date_range: Tuple[str, str]
) -> Iterator[IO[str]]:
    params = {
        "from_date": date_range[0],
        "to_date": date_range[1],
        "event": f'["{event}"]',
    }
    auth = (creds.api_secret, creds.token)
    result = _export(auth, params)
    with tempfile.NamedTemporaryFile("w+") as tmp:
        tmp.write(result.text)
        yield tmp


class ApiClient(NamedTuple):
    load_data: Callable[[str, Tuple[str, str]], Iterator[IO[str]]]
    data_handler: Callable[[str, Tuple[str, str]], ContextManager[IO[str]]]

    @classmethod
    def from_creds(cls, creds: Credentials) -> "ApiClient":
        @contextmanager
        def data_handler(
            event: str, date_range: Tuple[str, str]
        ) -> Iterator[IO[str]]:
            return _load_data(creds, event, date_range)

        return ApiClient(
            load_data=partial(_load_data, creds), data_handler=data_handler
        )
