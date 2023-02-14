from http_headers.common import (
    get_header_value_delimiter,
)
from http_headers.types import (
    ReferrerPolicyHeader,
)
from operator import (
    methodcaller,
)


def _is_referrer_policy(name: str) -> bool:
    return name.lower() == "referrer-policy"


def parse(line: str) -> ReferrerPolicyHeader | None:
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

    portions: list[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    # Get the name in `name: value`
    name = portions.pop(0)

    if not _is_referrer_policy(name):
        return None

    # Get the value in `name: value`
    values: list[str] = []
    if portions:
        value = portions.pop(0).lower()

        values = value.split(get_header_value_delimiter(value))
        values = list(map(methodcaller("strip"), values))
        values = list(filter(None, values))

    return ReferrerPolicyHeader(
        name=name,
        values=values,
    )
