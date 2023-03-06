from ._state import (
    encode_state,
)
from fa_purity import (
    Cmd,
    PureIter,
    Stream,
)
from fa_purity.pure_iter import (
    transform as PIterTransform,
)
from fa_purity.stream.transform import (
    chain,
    consume,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
)
import sys
from tap_checkly.singer import (
    ObjEncoder,
)
from tap_checkly.state import (
    EtlState,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def emit_items(
    records: PureIter[SingerRecord],
) -> Cmd[None]:
    emissions = records.map(lambda s: emitter.emit(sys.stdout, s))
    return PIterTransform.consume(emissions)


def emit_singer_records(
    records: Stream[SingerRecord] | PureIter[SingerRecord],
) -> Cmd[None]:
    if isinstance(records, Stream):
        emissions = records.map(lambda s: emitter.emit(sys.stdout, s))
        return consume(emissions)
    emissions_2 = records.map(lambda s: emitter.emit(sys.stdout, s))
    return PIterTransform.consume(emissions_2)


def from_encoder(
    encoder: ObjEncoder[_T], items: Stream[_T] | PureIter[_T]
) -> Cmd[None]:
    schemas = encoder.schemas.map(
        lambda s: emitter.emit(sys.stdout, s)
    ).transform(PIterTransform.consume)
    if isinstance(items, Stream):
        _data = items.map(encoder.record).transform(lambda x: chain(x))
        return schemas + emit_singer_records(_data)
    _data_2 = items.map(encoder.record).transform(
        lambda x: PIterTransform.chain(x)
    )
    return schemas + emit_singer_records(_data_2)


def emit_state(state: EtlState) -> Cmd[None]:
    return emitter.emit(sys.stdout, encode_state(state))
