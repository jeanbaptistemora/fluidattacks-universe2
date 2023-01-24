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


class SortsSuggestion(NamedTuple):
    finding_title: str
    probability: int


class ToeLinesState(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    attacked_lines: int
    be_present: bool
    be_present_until: Optional[datetime]
    comments: str
    first_attack_at: Optional[datetime]
    has_vulnerabilities: Optional[bool]
    last_author: str
    last_commit: str
    loc: int
    modified_by: str
    modified_date: datetime
    seen_at: datetime
    sorts_risk_level: int
    sorts_risk_level_date: Optional[datetime] = None
    sorts_suggestions: Optional[list[SortsSuggestion]] = None


class ToeLines(NamedTuple):
    filename: str
    group_name: str
    modified_date: datetime
    root_id: str
    state: ToeLinesState
    seen_first_time_by: Optional[str] = None

    def get_hash(self) -> int:
        return hash((self.group_name, self.root_id, self.filename))


class ToeLinesEdge(NamedTuple):
    node: ToeLines
    cursor: str


class ToeLinesConnection(NamedTuple):
    edges: tuple[ToeLinesEdge, ...]
    page_info: PageInfo
    total: Optional[int] = None


class ToeLinesMetadataToUpdate(NamedTuple):
    modified_date: Optional[datetime] = None
    clean_attacked_at: bool = False
    clean_be_present_until: bool = False
    clean_first_attack_at: bool = False


class ToeLinesRequest(NamedTuple):
    filename: str
    group_name: str
    root_id: str


class GroupToeLinesRequest(NamedTuple):
    group_name: str
    after: Optional[str] = None
    be_present: Optional[bool] = None
    first: Optional[int] = None
    paginate: bool = False


class RootToeLinesRequest(NamedTuple):
    group_name: str
    root_id: str
    after: Optional[str] = None
    be_present: Optional[bool] = None
    first: Optional[int] = None
    paginate: bool = False
