from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
)
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from typing import (
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class ObjEncoder(Generic[_T]):
    schemas: PureIter[SingerSchema]
    _records: _Patch[Callable[[_T], PureIter[SingerRecord]]]

    def record(self, item: _T) -> PureIter[SingerRecord]:
        return self._records.inner(item)

    @staticmethod
    def new(
        schemas: PureIter[SingerSchema],
        records: Callable[[_T], PureIter[SingerRecord]],
        _type: Optional[Type[_T]] = None,
    ) -> ObjEncoder[_T]:
        return ObjEncoder(schemas, _Patch(records))
