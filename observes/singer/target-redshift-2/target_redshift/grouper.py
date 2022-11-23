from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
    Stream,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from fa_purity.union import (
    Coproduct,
    CoproductFactory,
)
from fa_singer_io.singer import (
    SingerMessage,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from typing import (
    Callable,
    Iterable,
    List,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class PackagedSinger:
    _inner: Coproduct[
        PureIter[SingerRecord], Coproduct[SingerSchema, SingerState]
    ]

    @staticmethod
    def new(
        item: PureIter[SingerRecord] | SingerSchema | SingerState,
    ) -> PackagedSinger:
        factory: CoproductFactory[
            SingerSchema, SingerState
        ] = CoproductFactory()
        factory_2: CoproductFactory[
            PureIter[SingerRecord], Coproduct[SingerSchema, SingerState]
        ] = CoproductFactory()
        if isinstance(item, SingerSchema):
            return PackagedSinger(factory_2.inr(factory.inl(item)))
        if isinstance(item, SingerState):
            return PackagedSinger(factory_2.inr(factory.inr(item)))
        return PackagedSinger(factory_2.inl(item))

    def map(
        self,
        t1: Callable[[PureIter[SingerRecord]], _T],
        t2: Callable[[SingerSchema], _T],
        t3: Callable[[SingerState], _T],
    ) -> _T:
        return self._inner.map(t1, lambda c: c.map(t2, t3))


def _group(
    items: Iterable[SingerMessage], size: int
) -> Iterable[PackagedSinger]:
    accumulator: List[SingerRecord] = []
    for item in items:
        if isinstance(item, (SingerSchema, SingerState)):
            if accumulator:
                yield PackagedSinger.new(from_flist(freeze(accumulator)))
                accumulator = []
            yield PackagedSinger.new(item)
        else:
            accumulator.append(item)
            if len(accumulator) >= size:
                yield PackagedSinger.new(from_flist(freeze(accumulator)))
                accumulator = []
    if accumulator:
        yield PackagedSinger.new(from_flist(freeze(accumulator)))
        accumulator = []


def group_records(
    msgs: Stream[SingerMessage],
    size: int,
) -> Stream[PackagedSinger]:
    return unsafe_from_cmd(
        msgs.unsafe_to_iter().map(lambda i: _group(i, size))
    )
