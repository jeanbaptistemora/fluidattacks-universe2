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
    modified_by: Optional[str]
    modified_date: Optional[datetime]


class ToeLines(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    attacked_lines: int
    be_present: bool
    be_present_until: Optional[datetime]
    comments: str
    filename: str
    first_attack_at: Optional[datetime]
    has_vulnerabilities: Optional[bool]
    group_name: str
    last_author: str
    last_commit: str
    loc: int
    modified_date: datetime
    root_id: str
    seen_at: datetime
    sorts_risk_level: int
    state: ToeLinesState
    sorts_risk_level_date: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    sorts_suggestions: Optional[list[SortsSuggestion]] = None

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
    state: ToeLinesState
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    attacked_lines: Optional[int] = None
    be_present: Optional[bool] = None
    be_present_until: Optional[datetime] = None
    comments: Optional[str] = None
    first_attack_at: Optional[datetime] = None
    has_vulnerabilities: Optional[bool] = None
    last_author: Optional[str] = None
    last_commit: Optional[str] = None
    loc: Optional[int] = None
    modified_date: Optional[datetime] = None
    seen_at: Optional[datetime] = None
    sorts_risk_level: Optional[int] = None
    sorts_risk_level_date: Optional[datetime] = None
    clean_be_present_until: bool = False
    sorts_suggestions: Optional[list[SortsSuggestion]] = None


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
