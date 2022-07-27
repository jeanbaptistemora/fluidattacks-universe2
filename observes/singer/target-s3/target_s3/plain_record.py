from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    ResultE,
)
from fa_purity.json.primitive.core import (
    Primitive,
)
from fa_purity.json.value.core import (
    JsonValue,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_singer_io.singer import (
    SingerRecord,
)


@dataclass(frozen=True)
class _PlainRecord:
    data: FrozenDict[str, Primitive]
    record: SingerRecord


@dataclass(frozen=True)
class PlainRecord:
    """
    `SingerRecord` that has data on the form of `FrozenDict[str, Primitive]`
    """

    _inner: _PlainRecord

    @property
    def record(self) -> SingerRecord:
        return self._inner.record

    @property
    def data(self) -> FrozenDict[str, Primitive]:
        return self._inner.data

    @staticmethod
    def new(record: SingerRecord) -> ResultE[PlainRecord]:
        items = (
            Unfolder(JsonValue(record.record))
            .to_unfolder_dict()
            .map(lambda d: tuple(d.items()))
            .map(
                lambda t: tuple(
                    v.to_any_primitive().map(lambda x: (k, x)) for k, v in t
                )
            )
            .alt(Exception)
            .bind(lambda x: all_ok(x))
            .map(lambda x: FrozenDict(dict(x)))
        )
        return items.map(lambda d: PlainRecord(_PlainRecord(d, record)))
