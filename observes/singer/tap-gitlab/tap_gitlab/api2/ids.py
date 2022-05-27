from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from urllib.parse import (
    quote,
    unquote,
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
    user_id: str


@dataclass(frozen=True)
class _ProjectId:
    proj_id: str | int


@dataclass(frozen=True)
class ProjectId(_ProjectId):
    def __init__(self, obj: _ProjectId) -> None:
        super().__init__(obj.proj_id)

    @classmethod
    def from_name(cls, name: str) -> ProjectId:
        return ProjectId(_ProjectId(quote(name, safe="")))

    @classmethod
    def from_id(cls, proj_id: int) -> ProjectId:
        return ProjectId(_ProjectId(proj_id))

    @property
    def str_val(self) -> str:
        if isinstance(self.proj_id, str):
            return self.proj_id
        return str(self.proj_id)

    @property
    def raw(self) -> str | int:
        if isinstance(self.proj_id, str):
            return unquote(self.proj_id)
        return self.proj_id
