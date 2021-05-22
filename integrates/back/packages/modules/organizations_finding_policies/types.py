from typing import NamedTuple


class OrgFindingPolicy(NamedTuple):
    id: str
    last_status_update: str
    name: str
    status: str
