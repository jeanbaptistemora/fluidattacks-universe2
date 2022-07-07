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
from fa_singer_io.singer import (
    SingerMessage,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from typing import (
    Iterable,
    List,
    Union,
)

PackagedSinger = Union[SingerSchema, PureIter[SingerRecord], SingerState]


def _group(
    items: Iterable[SingerMessage], size: int
) -> Iterable[PackagedSinger]:
    accumulator: List[SingerRecord] = []
    for item in items:
        if isinstance(item, (SingerSchema, SingerState)):
            if accumulator:
                yield from_flist(freeze(accumulator))
                accumulator = []
            yield item
        else:
            accumulator.append(item)
            if len(accumulator) >= size:
                yield from_flist(freeze(accumulator))
                accumulator = []
    if accumulator:
        yield from_flist(freeze(accumulator))
        accumulator = []


def group_records(
    msgs: Stream[SingerMessage],
    size: int,
) -> Stream[PackagedSinger]:
    return unsafe_from_cmd(
        msgs.unsafe_to_iter().map(lambda i: _group(i, size))
    )
