from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
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


@dataclass(frozen=True)
class ProjectId:
    proj_id: Union[str, int]

    def __init__(self, obj: _ProjectId) -> None:
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)

    @classmethod
    def from_name(cls, name: str) -> ProjectId:
        return ProjectId(_ProjectId(quote(name, safe="")))

    @classmethod
    def from_id(cls, proj_id: int) -> ProjectId:
        return ProjectId(_ProjectId(proj_id))
