# Standard libraries
from contextlib import contextmanager
import tempfile
from typing import (
    Any,
    Dict,
    IO,
    Iterator,
    Tuple,
)
# Third party libraries
from ratelimiter import RateLimiter
import requests
# Local libraries


JSON = Dict[str, Any]
API_BASE_URL = 'https://data.mixpanel.com/api/2.0'
rate_limiter = RateLimiter(max_calls=40, period=3600)


def export(auth: Tuple[str, str], params: JSON) -> Any:
    with rate_limiter:
        return requests.get(
            f'{API_BASE_URL}/export/',
            auth=auth,
            params=params
        )


@contextmanager
def load_data(event: str, credentials: Dict[str, Any]) -> Iterator[IO[str]]:
    from_date = credentials['from_date']
    to_date = credentials['to_date']
    params = {
        "from_date": from_date,
        "to_date": to_date,
        "event": f'["{event}"]'
    }
    auth = (credentials['API_secret'], credentials['token'])
    result = export(auth, params)
    with tempfile.NamedTemporaryFile('w+') as tmp:
        tmp.write(result.text)
        yield tmp
