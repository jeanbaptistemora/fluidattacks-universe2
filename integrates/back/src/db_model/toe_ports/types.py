from datetime import (
    datetime,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
    Optional,
    Tuple,
)


class ToePortState(NamedTuple):
    modified_date: Optional[datetime]


class ToePort(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: Optional[str]
    be_present: bool
    be_present_until: Optional[datetime]
    first_attack_at: Optional[datetime]
    group_name: str
    has_vulnerabilities: bool
    address: str
    port: str
    root_id: str
    seen_at: Optional[datetime]
    seen_first_time_by: Optional[str]

    def get_hash(self) -> int:
        return hash((self.group_name, self.address, self.port))


class ToePortEdge(NamedTuple):
    node: ToePort
    cursor: str


class ToePortsConnection(NamedTuple):
    edges: Tuple[ToePortEdge, ...]
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


class ToePortMetadataToUpdate(NamedTuple):
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    be_present: Optional[bool] = None
    be_present_until: Optional[datetime] = None
    first_attack_at: Optional[datetime] = None
    has_vulnerabilities: Optional[bool] = None
    seen_at: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    clean_attacked_at: bool = False
    clean_be_present_until: bool = False
    clean_first_attack_at: bool = False
    clean_seen_at: bool = False
