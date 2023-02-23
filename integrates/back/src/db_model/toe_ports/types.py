from datetime import (
    datetime,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
)


class ToePortState(NamedTuple):
    attacked_at: datetime | None
    attacked_by: str | None
    be_present: bool
    be_present_until: datetime | None
    first_attack_at: datetime | None
    has_vulnerabilities: bool
    modified_by: str | None
    modified_date: datetime | None


class ToePort(NamedTuple):
    group_name: str
    address: str
    port: str
    root_id: str
    state: ToePortState
    seen_at: datetime | None
    seen_first_time_by: str | None

    def get_hash(self) -> int:
        return hash((self.group_name, self.address, self.port))


class ToePortEdge(NamedTuple):
    node: ToePort
    cursor: str


class ToePortsConnection(NamedTuple):
    edges: tuple[ToePortEdge, ...]
    page_info: PageInfo


class ToePortRequest(NamedTuple):
    group_name: str
    address: str
    port: str
    root_id: str


class GroupToePortsRequest(NamedTuple):
    group_name: str
    after: str | None = None
    be_present: bool | None = None
    first: int | None = None
    paginate: bool = False


class RootToePortsRequest(NamedTuple):
    group_name: str
    root_id: str
    after: str | None = None
    be_present: bool | None = None
    first: int | None = None
    paginate: bool = False
