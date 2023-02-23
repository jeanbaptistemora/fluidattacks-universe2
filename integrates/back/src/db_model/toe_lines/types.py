from datetime import (
    datetime,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
)


class SortsSuggestion(NamedTuple):
    finding_title: str
    probability: int


class ToeLinesState(NamedTuple):
    attacked_at: datetime | None
    attacked_by: str
    attacked_lines: int
    be_present: bool
    be_present_until: datetime | None
    comments: str
    first_attack_at: datetime | None
    has_vulnerabilities: bool | None
    last_author: str
    last_commit: str
    last_commit_date: datetime
    loc: int
    modified_by: str
    modified_date: datetime
    seen_at: datetime
    sorts_risk_level: int
    sorts_risk_level_date: datetime | None = None
    sorts_suggestions: list[SortsSuggestion] | None = None


class ToeLines(NamedTuple):
    filename: str
    group_name: str
    modified_date: datetime
    root_id: str
    state: ToeLinesState
    seen_first_time_by: str | None = None


class ToeLinesEdge(NamedTuple):
    node: ToeLines
    cursor: str


class ToeLinesConnection(NamedTuple):
    edges: tuple[ToeLinesEdge, ...]
    page_info: PageInfo
    total: int | None = None


class ToeLinesMetadataToUpdate(NamedTuple):
    modified_date: datetime | None = None
    clean_attacked_at: bool = False
    clean_be_present_until: bool = False
    clean_first_attack_at: bool = False


class ToeLinesRequest(NamedTuple):
    filename: str
    group_name: str
    root_id: str


class GroupToeLinesRequest(NamedTuple):
    group_name: str
    after: str | None = None
    be_present: bool | None = None
    first: int | None = None
    paginate: bool = False


class RootToeLinesRequest(NamedTuple):
    group_name: str
    root_id: str
    after: str | None = None
    be_present: bool | None = None
    first: int | None = None
    paginate: bool = False
