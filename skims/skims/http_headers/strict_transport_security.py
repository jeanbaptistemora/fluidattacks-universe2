# Standard library
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)

from http_headers.types import (
    StrictTransportSecurityHeader,
)


def _is_strict_transport_security(name: str) -> bool:
    return name.lower() == "strict-transport-security"


def _parse_max_age(token: str) -> Optional[int]:
    portions = token.split("=", maxsplit=1)

    if len(portions) == 2:
        try:
            return int(portions[1].strip())
        except ValueError:
            # Max age is not an integer
            return None
    return None


def parse(line: str) -> Optional[StrictTransportSecurityHeader]:
    # Strict-Transport-Security: max-age=<expire-time>
    # Strict-Transport-Security: max-age=<expire-time>; includeSubDomains
    # Strict-Transport-Security: max-age=<expire-time>; preload
    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    if len(portions) != 2:
        return None

    name, value = portions

    if not _is_strict_transport_security(name):
        return None

    include_sub_domains: Optional[bool] = None
    max_age: Optional[int] = None
    preload: Optional[bool] = None

    portions = value.split(";")
    portions = list(map(methodcaller("strip"), portions))
    portions = list(map(methodcaller("lower"), portions))

    for portion in portions:
        if portion == "preload":
            preload = True
        elif portion == "includesubdomains":
            include_sub_domains = True
        elif portion.startswith("max-age"):
            max_age = _parse_max_age(portion)

    if max_age is None:
        return None

    return StrictTransportSecurityHeader(
        name=name,
        include_sub_domains=include_sub_domains,
        max_age=max_age,
        preload=preload,
    )
