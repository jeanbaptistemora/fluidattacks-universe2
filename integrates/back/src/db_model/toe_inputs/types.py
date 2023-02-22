from datetime import (
    datetime,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
)


class ToeInputState(NamedTuple):
    attacked_at: datetime | None
    attacked_by: str
    be_present: bool
    be_present_until: datetime | None
    first_attack_at: datetime | None
    has_vulnerabilities: bool | None
    modified_by: str
    modified_date: datetime
    seen_at: datetime | None
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
    after: str | None = None
    be_present: bool | None = None
    first: int | None = None
    paginate: bool = False


class RootToeInputsRequest(NamedTuple):
    group_name: str
    root_id: str
    after: str | None = None
    be_present: bool | None = None
    first: int | None = None
    paginate: bool = False


class ToeInputMetadataToUpdate(NamedTuple):
    clean_attacked_at: bool = False
    clean_be_present_until: bool = False
    clean_first_attack_at: bool = False
    clean_seen_at: bool = False
