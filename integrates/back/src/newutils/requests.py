from custom_exceptions import (
    InvalidSource,
)
from db_model.enums import (
    Source,
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


def get_source_new(context: Any) -> Source:
    source = get_source(context)
    return Source[source.upper()]
