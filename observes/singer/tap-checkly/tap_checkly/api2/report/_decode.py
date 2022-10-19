# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    JsonObj,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from tap_checkly.api2._utils import (
    ExtendedUnfolder,
)
from tap_checkly.objs import (
    CheckId,
    CheckReport,
)


@dataclass(frozen=True)
class _Aggregate:
    avg: float
    p95: float
    p99: float
    success_ratio: float


def _decode_aggregate(raw: JsonObj) -> ResultE[_Aggregate]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.require_float("avg").bind(
        lambda avg: unfolder.require_float("p95").bind(
            lambda p95: unfolder.require_float("p99").bind(
                lambda p99: unfolder.require_float("successRatio").map(
                    lambda success_ratio: _Aggregate(
                        avg, p95, p99, success_ratio
                    )
                )
            )
        )
    )


@dataclass(frozen=True)
class CheckReportDecoder:
    raw: JsonObj

    def decode_report(self) -> ResultE[CheckReport]:
        unfolder = ExtendedUnfolder(self.raw)
        aggregate = (
            unfolder.get_required("aggregate")
            .bind(lambda u: Unfolder(u).to_json().alt(Exception))
            .bind(_decode_aggregate)
        )
        return (
            unfolder.require_primitive("checkId", str)
            .map(CheckId)
            .bind(
                lambda check_id: unfolder.require_primitive(
                    "checkType", str
                ).bind(
                    lambda check_type: unfolder.require_primitive(
                        "deactivated", bool
                    ).bind(
                        lambda deactivated: unfolder.require_primitive(
                            "name", str
                        ).bind(
                            lambda name: aggregate.map(
                                lambda agg: CheckReport(
                                    check_id,
                                    check_type,
                                    deactivated,
                                    name,
                                    agg.avg,
                                    agg.p95,
                                    agg.p99,
                                    agg.success_ratio,
                                )
                            )
                        )
                    )
                )
            )
        )
