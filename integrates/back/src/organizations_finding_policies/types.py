from typing import (
    NamedTuple,
    Set,
)


class OrgFindingPolicy(NamedTuple):
    # pylint: disable=too-few-public-methods, inherit-non-class
    id: str
    last_status_update: str
    name: str
    status: str
    tags: Set[str]
