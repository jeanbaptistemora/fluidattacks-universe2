# Standard libraries
from typing import (
    NamedTuple,
)

# Third party libraries

# Local libraries
from tap_mailchimp.common.objs import (
    JSON
)


class Credentials(NamedTuple):
    api_key: str
    dc: str


def to_credentials(raw: JSON) -> Credentials:
    return Credentials(
        api_key=raw['api_key'],
        dc=raw['dc']
    )
