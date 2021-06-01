from http_headers.types import (
    XContentTypeOptionsHeader,
)
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)


def _is_x_content_type_options(name: str) -> bool:
    return name.lower() == "x-content-type-options"


def parse(line: str) -> Optional[XContentTypeOptionsHeader]:
    # X-Content-Type-Options: nosniff
    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    if len(portions) != 2:
        return None

    name, value = portions

    if not _is_x_content_type_options(name):
        return None

    return XContentTypeOptionsHeader(
        name=name,
        value=value.lower(),
    )
