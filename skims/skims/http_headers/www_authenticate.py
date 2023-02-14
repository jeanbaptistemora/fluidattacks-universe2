from http_headers.types import (
    WWWAuthenticate,
)
from operator import (
    methodcaller,
)
import re

REGEX = re.compile(
    r"^(?P<type>\w+)\s+"
    r"realm=(?P<realm>.*?)"
    r"(?:,\s+charset=(?P<charset>.*?))?$"
)


def _is_www_authenticate(name: str) -> bool:
    return name.lower() == "www-authenticate"


def parse(line: str) -> WWWAuthenticate | None:
    # WWW-Authenticate: <type> realm=<realm>[, charset="UTF-8"]
    portions: list[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    if len(portions) != 2:
        return None

    name, value = portions

    if not _is_www_authenticate(name):
        return None

    if match := REGEX.match(value):
        groups = match.groupdict()
        return WWWAuthenticate(
            name=name,
            charset=groups["charset"] or "",
            type=groups["type"].lower(),
            realm=groups["realm"],
        )

    return None
