from typing import (
    NamedTuple,
)


class Portal(NamedTuple):
    group: str
    portal_url: str
    return_url: str
