from dynamodb.types import (
    PageInfo,
)
from typing import (
    NamedTuple,
    Optional,
    Tuple,
)


class ToeLines(NamedTuple):
    attacked_at: str
    attacked_by: str
    attacked_lines: int
    be_present: bool
    be_present_until: str
    comments: str
    commit_author: str
    filename: str
    first_attack_at: str
    group_name: str
    is_deactivated: bool
    loc: int
    modified_commit: str
    modified_date: str
    root_id: str
    seen_at: str
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
    attacked_at: Optional[str] = None
    attacked_by: Optional[str] = None
    attacked_lines: Optional[int] = None
    be_present: Optional[bool] = None
    be_present_until: Optional[str] = None
    comments: Optional[str] = None
    commit_author: Optional[str] = None
    first_attack_at: Optional[str] = None
    is_deactivated: Optional[bool] = None
    loc: Optional[int] = None
    modified_commit: Optional[str] = None
    modified_date: Optional[str] = None
    seen_at: Optional[str] = None
    sorts_risk_level: Optional[int] = None


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
