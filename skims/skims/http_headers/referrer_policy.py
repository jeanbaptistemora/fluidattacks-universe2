# Standard libraryes
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)

# Third party libraries
from http_headers.types import (
    ReferrerPolicyHeader,
)


def _is_referrer_policy(name: str) -> bool:
    return name.lower() == "referrer-policy"


def parse(line: str) -> Optional[ReferrerPolicyHeader]:
    # Referrer-Policy: no-referrer
    # Referrer-Policy: no-referrer-when-downgrade
    # Referrer-Policy: origin
    # Referrer-Policy: origin-when-cross-origin
    # Referrer-Policy: same-origin
    # Referrer-Policy: strict-origin
    # Referrer-Policy: strict-origin-when-cross-origin
    # Referrer-Policy: unsafe-url
    #
    # Can also be set as a comma separated list

    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    # Get the name in `name: value`
    name = portions.pop(0)

    if not _is_referrer_policy(name):
        return None

    # Get the value in `name: value`
    values: List[str]
    if portions:
        value = portions.pop(0).lower()
        values = value.split(",")
        values = list(map(methodcaller("strip"), values))
        values = list(filter(None, values))
    else:
        values = []

    return ReferrerPolicyHeader(
        name=name,
        values=values,
    )
