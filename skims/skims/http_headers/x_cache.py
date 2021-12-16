from http_headers.types import (
    XCacheHeader,
)
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)


def _is_x_cache(name: str) -> bool:
    return name.lower() == "x-cache"


def parse(line: str) -> Optional[XCacheHeader]:
    # X-Cache: Hit from CDN
    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not _is_x_cache(name):
        return None

    return XCacheHeader(
        name=name,
        value=value,
    )
