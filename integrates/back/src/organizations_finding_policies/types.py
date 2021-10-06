from typing import (
    NamedTuple,
    Set,
)


class OrgFindingPolicy(NamedTuple):
    id: str
    last_status_update: str
    name: str
    status: str
    tags: Set[str]
