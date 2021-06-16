from __future__ import (
    annotations,
)

from returns.primitives.types import (
    Immutable,
)
from typing import (
    NamedTuple,
    Union,
)
from urllib.parse import (
    quote,
)


class _ProjectId(NamedTuple):
    proj_id: Union[str, int]


class ProjectId(Immutable):
    proj_id: Union[str, int]

    def __new__(cls, obj: _ProjectId) -> ProjectId:
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    @classmethod
    def from_name(cls, name: str) -> ProjectId:
        return ProjectId(_ProjectId(quote(name, safe="")))

    @classmethod
    def from_id(cls, proj_id: int) -> ProjectId:
        return ProjectId(_ProjectId(proj_id))
