from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Result,
    ResultE,
)
import re


@dataclass(frozen=True)
class _GroupId:
    name: str


@dataclass(frozen=True)
class GroupId:
    _inner: _GroupId

    @property
    def name(self) -> str:
        return self._inner.name

    @staticmethod
    def new(name: str) -> ResultE[GroupId]:
        _name = name.removeprefix("GROUP#")
        pattern = "^[\w\s-]+$"
        if not re.match(pattern, _name):
            err = ValueError(f"Group name is not `^[\w- ]+$` i.e. {_name}")
            return Result.failure(err)
        return Result.success(_GroupId(_name), Exception).map(GroupId)
