from http_headers.types import (
    XCacheHeader,
)
from operator import (
    methodcaller,
)


def _is_x_cache(name: str) -> bool:
    return name.lower() == "x-cache"


def parse(line: str) -> XCacheHeader | None:
    # X-Cache: Hit from CDN
    portions: list[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not _is_x_cache(name):
        return None

    return XCacheHeader(
        name=name,
        value=value,
    )
