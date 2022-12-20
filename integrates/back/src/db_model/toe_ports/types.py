from datetime import (
    datetime,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
    Optional,
)


class ToePortState(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: Optional[str]
    be_present: bool
    be_present_until: Optional[datetime]
    first_attack_at: Optional[datetime]
    has_vulnerabilities: bool
    modified_by: Optional[str]
    modified_date: Optional[datetime]


class ToePort(NamedTuple):
    group_name: str
    address: str
    port: str
    root_id: str
    state: ToePortState
    seen_at: Optional[datetime]
    seen_first_time_by: Optional[str]

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
    after: Optional[str] = None
    be_present: Optional[bool] = None
    first: Optional[int] = None
    paginate: bool = False


class RootToePortsRequest(NamedTuple):
    group_name: str
    root_id: str
    after: Optional[str] = None
    be_present: Optional[bool] = None
    first: Optional[int] = None
    paginate: bool = False
