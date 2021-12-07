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


class ToeLines(NamedTuple):
    attacked_at: Optional[datetime]
    attacked_by: str
    attacked_lines: int
    be_present: bool
    be_present_until: Optional[datetime]
    comments: str
    commit_author: str
    filename: str
    first_attack_at: Optional[datetime]
    group_name: str
    loc: int
    modified_commit: str
    modified_date: datetime
    root_id: str
    seen_at: datetime
    sorts_risk_level: int

    def get_hash(self) -> int:
        return hash((self.group_name, self.root_id, self.filename))


class ToeLinesEdge(NamedTuple):
    node: ToeLines
    cursor: str


class ToeLinesConnection(NamedTuple):
    edges: Tuple[ToeLinesEdge, ...]
    page_info: PageInfo


class ToeLinesMetadataToUpdate(NamedTuple):
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    attacked_lines: Optional[int] = None
    be_present: Optional[bool] = None
    be_present_until: Optional[datetime] = None
    comments: Optional[str] = None
    commit_author: Optional[str] = None
    first_attack_at: Optional[datetime] = None
    loc: Optional[int] = None
    modified_commit: Optional[str] = None
    modified_date: Optional[datetime] = None
    seen_at: Optional[datetime] = None
    sorts_risk_level: Optional[int] = None
    clean_be_present_until: bool = False


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
