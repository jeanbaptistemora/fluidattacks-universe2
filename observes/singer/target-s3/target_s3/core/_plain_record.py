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
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_singer_io.singer import (
    SingerRecord,
)


@dataclass(frozen=True)
class _PlainRecord:
    stream: str
    record: FrozenDict[str, Primitive]


@dataclass(frozen=True)
class PlainRecord:
    _inner: _PlainRecord

    @property
    def stream(self) -> str:
        return self._inner.stream

    @property
    def record(self) -> FrozenDict[str, Primitive]:
        return self._inner.record

    @staticmethod
    def from_singer(record: SingerRecord) -> ResultE[PlainRecord]:
        items = (
            Unfolder(JsonValue(record.record))
            .to_unfolder_dict()
            .map(lambda d: tuple(d.items()))
            .map(
                lambda t: tuple(
                    pure_map(
                        lambda p: p[1]
                        .to_any_primitive()
                        .map(lambda x: (p[0], x)),
                        t,
                    )
                )
            )
            .alt(Exception)
            .bind(lambda x: all_ok(x))
            .map(lambda x: FrozenDict(dict(x)))
        )
        return items.map(lambda d: PlainRecord(_PlainRecord(record.stream, d)))

    @staticmethod
    def new(stream: str, record: FrozenDict[str, Primitive]) -> PlainRecord:
        return PlainRecord(_PlainRecord(stream, record))
