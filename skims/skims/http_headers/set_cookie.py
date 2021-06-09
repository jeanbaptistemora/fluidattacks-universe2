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

    raw_portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), raw_portions))

    name = portions[0]

    if not _is_set_cookie(name):
        return None

    raw_content = portions[1]

    attributes: List[str] = raw_content.split(";")
    attributes = list(map(methodcaller("strip"), attributes))

    cookie, parameters = attributes[0], attributes[1:]

    content: List[str] = cookie.split("=", maxsplit=1)
    content = list(map(methodcaller("strip"), content))

    cookie_name = content[0]
    cookie_value = content[1]

    secure = False

    for parameter in parameters:
        if parameter.lower() == "secure":
            secure = True

    return SetCookieHeader(
        name=name,
        raw_content=raw_content,
        cookie_name=cookie_name,
        cookie_value=cookie_value,
        secure=secure,
    )
