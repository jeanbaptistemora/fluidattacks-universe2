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
from tap_checkly.api._utils import (
    ExtendedUnfolder,
)
from tap_checkly.objs import (
    CheckId,
    CheckStatus,
    CheckStatusObj,
    IndexedObj,
)


@dataclass(frozen=True)
class CheckStatusDecoder:
    raw: JsonObj

    def decode_check(self) -> ResultE[CheckStatus]:
        unfolder = ExtendedUnfolder(self.raw)
        return unfolder.require_primitive("name", str).bind(
            lambda name: unfolder.require_datetime("created_at").bind(
                lambda created_at: unfolder.require_primitive(
                    "hasErrors", bool
                ).bind(
                    lambda has_errors: unfolder.require_primitive(
                        "hasFailures", bool
                    ).bind(
                        lambda has_failures: unfolder.require_primitive(
                            "isDegraded", bool
                        ).bind(
                            lambda is_degraded: unfolder.require_primitive(
                                "lastCheckRunId", str
                            ).bind(
                                lambda last_check_run_id: unfolder.require_primitive(
                                    "lastRunLocation", str
                                ).bind(
                                    lambda last_run_location: unfolder.require_primitive(
                                        "longestRun", int
                                    ).bind(
                                        lambda longest_run: unfolder.require_primitive(
                                            "shortestRun", int
                                        ).bind(
                                            lambda shortest_run: unfolder.maybe_primitive(
                                                "sslDaysRemaining", int
                                            ).bind(
                                                lambda ssl_days_remaining: unfolder.opt_datetime(
                                                    "updated_at"
                                                ).map(
                                                    lambda updated_at: CheckStatus(
                                                        name,
                                                        created_at,
                                                        has_errors,
                                                        has_failures,
                                                        is_degraded,
                                                        last_check_run_id,
                                                        last_run_location,
                                                        longest_run,
                                                        shortest_run,
                                                        ssl_days_remaining,
                                                        updated_at,
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

    def decode_id(self) -> ResultE[CheckId]:
        unfolder = ExtendedUnfolder(self.raw)
        return unfolder.require_primitive("checkId", str).map(CheckId)

    def decode_obj(self) -> ResultE[CheckStatusObj]:
        return self.decode_id().bind(
            lambda cid: self.decode_check().map(lambda c: IndexedObj(cid, c))
        )
