# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0
from fa_purity import (
    FrozenDict,
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
    ExtendedUnfolder,
)
from tap_checkly.state import (
    EtlState,
)


def encode(state: EtlState) -> JsonObj:
    return FrozenDict(
        {
            "results_recent": JsonValue(
                state.results_recent.map(lambda d: d.isoformat()).value_or(
                    None
                )
            ),
            "results_oldest": JsonValue(
                state.results_oldest.map(lambda d: d.isoformat()).value_or(
                    None
                )
            ),
        }
    )


def encode_state(state: EtlState) -> SingerState:
    return SingerState(encode(state))


def decode(raw: JsonObj) -> ResultE[EtlState]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.opt_datetime("results_recent").bind(
        lambda recent: unfolder.opt_datetime("results_oldest").map(
            lambda oldest: EtlState(recent, oldest)
        )
    )
