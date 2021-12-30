from typing import (
    NamedTuple,
)


class Portal(NamedTuple):
    organization: str
    portal_url: str
    return_url: str
