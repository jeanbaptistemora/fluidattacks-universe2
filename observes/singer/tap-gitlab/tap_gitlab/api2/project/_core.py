from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from tap_gitlab.api2._utils import (
    int_to_str,
    str_to_int,
)
from urllib.parse import (
    quote,
    unquote,
)


@dataclass(frozen=True)
class _ProjectId:
    proj_id: str | int


@dataclass(frozen=True)
class ProjectId:
    inner: _ProjectId

    @classmethod
    def from_name(cls, name: str) -> ProjectId:
        return ProjectId(_ProjectId(quote(name, safe="")))

    @classmethod
    def from_num(cls, proj_id: int) -> ProjectId:
        return ProjectId(_ProjectId(proj_id))

    @classmethod
    def from_raw_str(cls, proj: str) -> ProjectId:
        _proj = str_to_int(proj).value_or(proj)
        if isinstance(_proj, int):
            return cls.from_num(_proj)
        return cls.from_name(_proj)

    @property
    def raw(self) -> str | int:
        if isinstance(self.inner.proj_id, str):
            return unquote(self.inner.proj_id)
        return self.inner.proj_id

    def to_str(self) -> str:
        if isinstance(self.raw, int):
            return int_to_str(self.raw)
        return self.raw
