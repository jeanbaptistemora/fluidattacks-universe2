from ._state import (
    encode_state,
)
from fa_purity import (
    Cmd,
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


def emit_stream(
    records: Stream[SingerRecord],
) -> Cmd[None]:
    emissions = records.map(lambda s: emitter.emit(sys.stdout, s))
    return consume(emissions)


def from_encoder(encoder: ObjEncoder[_T], items: Stream[_T]) -> Cmd[None]:
    schemas = encoder.schemas.map(
        lambda s: emitter.emit(sys.stdout, s)
    ).transform(PIterTransform.consume)
    return schemas + emit_stream(items.map(encoder.record).transform(chain))


def emit_state(state: EtlState) -> Cmd[None]:
    return emitter.emit(sys.stdout, encode_state(state))
