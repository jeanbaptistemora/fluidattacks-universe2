from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class EpicId:
    global_id: str
    internal_id: int


@dataclass(frozen=True)
class IssueId:
    global_id: str
    internal_id: int


@dataclass(frozen=True)
class MilestoneId:
    global_id: str
    internal_id: int


@dataclass(frozen=True)
class UserId:
    global_id: str
    internal_id: int
