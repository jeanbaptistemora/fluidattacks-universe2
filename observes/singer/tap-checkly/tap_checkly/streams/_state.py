# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0
from fa_purity import (
    FrozenDict,
    Maybe,
    ResultE,
)
from fa_purity.json import (
    JsonObj,
    JsonValue,
)
from fa_singer_io.singer import (
    SingerState,
)
from tap_checkly._utils import (
    DateInterval,
    ExtendedUnfolder,
    switch_maybe,
)
from tap_checkly.state import (
    EtlState,
)


def _encode_interval(interval: DateInterval) -> JsonObj:
    return FrozenDict(
        {
            "newest": JsonValue(interval.newest.isoformat()),
            "oldest": JsonValue(interval.oldest.isoformat()),
        }
    )


def encode(state: EtlState) -> JsonObj:
    return FrozenDict(
        {
            "results": JsonValue(
                state.results.map(_encode_interval).value_or(None)
            ),
        }
    )


def encode_state(state: EtlState) -> SingerState:
    return SingerState(encode(state))


def _decode_interval(raw: JsonObj) -> ResultE[DateInterval]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.require_datetime("newest").bind(
        lambda newest: unfolder.require_datetime("oldest").bind(
            lambda oldest: DateInterval.new(oldest, newest)
        )
    )


def decode(raw: JsonObj) -> ResultE[EtlState]:
    unfolder = ExtendedUnfolder(raw)
    return (
        unfolder.require_opt_json("results")
        .map(lambda m: Maybe.from_optional(m).map(_decode_interval))
        .bind(lambda m: switch_maybe(m).map(lambda d: EtlState(d)))
    )
