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


class ToeInput(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    be_present: bool
    be_present_until: Optional[datetime]
    component: str
    entry_point: str
    first_attack_at: Optional[datetime]
    group_name: str
    seen_at: datetime
    seen_first_time_by: str
    unreliable_root_id: str

    def get_hash(self) -> int:
        return hash((self.group_name, self.component, self.entry_point))


class ToeInputEdge(NamedTuple):
    node: ToeInput
    cursor: str


class ToeInputsConnection(NamedTuple):
    edges: Tuple[ToeInputEdge, ...]
    page_info: PageInfo


class GroupToeInputsRequest(NamedTuple):
    group_name: str
    after: Optional[str] = None
    be_present: Optional[bool] = None
    first: Optional[int] = None
    paginate: bool = False
