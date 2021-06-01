from custom_exceptions import (
    InvalidSource,
)
from typing import (
    Any,
)


def get_source(context: Any) -> str:
    headers = context.headers
    source = headers.get("x-integrates-source", "integrates")
    if source not in {"integrates", "skims"}:
        raise InvalidSource()
    return source
