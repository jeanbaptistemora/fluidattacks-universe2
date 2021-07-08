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
    source: str = headers.get("x-integrates-source", "asm")
    # Compatibility with old API
    mapped_source: str = map_source(source)
    if mapped_source not in {"asm", "machine"}:
        raise InvalidSource()
    return mapped_source


def get_source_new(context: Any) -> Source:
    source = get_source(context)
    return Source[source.upper()]


def map_source(source: str) -> str:
    if source == "integrates":
        return "asm"
    if source == "skims":
        return "machine"
    return source
