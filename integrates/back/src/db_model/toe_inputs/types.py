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


class ToeInputState(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    be_present: bool
    be_present_until: Optional[datetime]
    first_attack_at: Optional[datetime]
    has_vulnerabilities: Optional[bool]
    modified_by: str
    modified_date: datetime
    seen_at: Optional[datetime]
    seen_first_time_by: str
    unreliable_root_id: str


class ToeInput(NamedTuple):
    component: str
    entry_point: str
    group_name: str
    state: ToeInputState

    def get_hash(self) -> int:
        return hash((self.group_name, self.component, self.entry_point))


class ToeInputEdge(NamedTuple):
    node: ToeInput
    cursor: str


class ToeInputsConnection(NamedTuple):
    edges: tuple[ToeInputEdge, ...]
    page_info: PageInfo


class ToeInputRequest(NamedTuple):
    component: str
    entry_point: str
    group_name: str
    root_id: str


class GroupToeInputsRequest(NamedTuple):
    group_name: str
    after: Optional[str] = None
    be_present: Optional[bool] = None
    first: Optional[int] = None
    paginate: bool = False


class RootToeInputsRequest(NamedTuple):
    group_name: str
    root_id: str
    after: Optional[str] = None
    be_present: Optional[bool] = None
    first: Optional[int] = None
    paginate: bool = False


class ToeInputMetadataToUpdate(NamedTuple):
    clean_attacked_at: bool = False
    clean_be_present_until: bool = False
    clean_first_attack_at: bool = False
    clean_seen_at: bool = False
