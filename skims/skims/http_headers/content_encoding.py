from http_headers.types import (
    ContentEncodingHeader,
)
from operator import (
    methodcaller,
)


def _is_content_encoding(name: str) -> bool:
    return name.lower() == "content-encoding"


def parse(line: str) -> ContentEncodingHeader | None:
    portions: list[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not _is_content_encoding(name):
        return None

    return ContentEncodingHeader(
        name=name,
        value=value,
    )
