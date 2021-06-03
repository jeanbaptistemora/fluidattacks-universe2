from http_headers.types import (
    SetCookieHeader,
)
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)


def _is_set_cookie(name: str) -> bool:
    return name.lower() == "set-cookie"


def parse(line: str) -> Optional[SetCookieHeader]:
    # Set-Cookie: <cookie-name>=<cookie-value>; Secure
    # Set-Cookie: <cookie-name>=<cookie-value>; HttpOnly

    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    # Get the name in `name: value`
    name = portions[0]

    if not _is_set_cookie(name):
        return None

    header = portions[1]

    attributes: List[str] = header.split(";")
    attributes = list(map(methodcaller("strip"), attributes))

    secure = False

    for attribute in attributes[1:]:
        if attribute.lower() == "secure":
            secure = True

    return SetCookieHeader(
        name=name,
        cookie=attributes[0],
        secure=secure,
    )
