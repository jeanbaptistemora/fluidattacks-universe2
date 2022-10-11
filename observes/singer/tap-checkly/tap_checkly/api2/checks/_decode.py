# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    Check,
    CheckConf1,
    CheckConf2,
    CheckObj,
)
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
    isoparse,
)
from tap_checkly.api2.id_objs import (
    CheckGroupId,
    CheckId,
    IndexedObj,
)


def _decode_conf_1(raw: JsonObj) -> ResultE[CheckConf1]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.require_primitive("activated", bool).bind(
        lambda activated: unfolder.require_primitive("muted", bool).bind(
            lambda muted: unfolder.require_primitive("doubleCheck", bool).bind(
                lambda double_check: unfolder.require_primitive(
                    "sslCheck", bool
                ).bind(
                    lambda ssl_check: unfolder.require_primitive(
                        "shouldFail", bool
                    ).bind(
                        lambda should_fail: unfolder.require_primitive(
                            "useGlobalAlertSettings", bool
                        ).map(
                            lambda global_alert: CheckConf1(
                                activated,
                                muted,
                                double_check,
                                ssl_check,
                                should_fail,
                                global_alert,
                            )
                        )
                    )
                )
            )
        )
    )


def _decode_conf_2(raw: JsonObj) -> ResultE[CheckConf2]:
    unfolder = ExtendedUnfolder(raw)
    return (
        unfolder.require_primitive("groupId", str)
        .map(CheckGroupId)
        .bind(
            lambda group_id: unfolder.require_primitive(
                "groupOrder", int
            ).bind(
                lambda group_order: unfolder.require_primitive(
                    "runtimeId", str
                ).bind(
                    lambda runtime_ver: unfolder.require_primitive(
                        "checkType", str
                    ).bind(
                        lambda check_type: unfolder.require_primitive(
                            "frequency", int
                        ).bind(
                            lambda frequency: unfolder.require_primitive(
                                "frequencyOffset", int
                            ).bind(
                                lambda frequency_offset: unfolder.require_primitive(
                                    "degradedResponseTime", int
                                ).bind(
                                    lambda degraded_response_time: unfolder.require_primitive(
                                        "maxResponseTime", int
                                    ).map(
                                        lambda max_response_time: CheckConf2(
                                            group_id,
                                            group_order,
                                            runtime_ver,
                                            check_type,
                                            frequency,
                                            frequency_offset,
                                            degraded_response_time,
                                            max_response_time,
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


@dataclass(frozen=True)
class CheckDecoder:
    raw: JsonObj

    def decode_check(self) -> ResultE[Check]:
        unfolder = ExtendedUnfolder(self.raw)
        return unfolder.require_primitive("name", str).bind(
            lambda name: _decode_conf_1(self.raw).bind(
                lambda conf_1: _decode_conf_2(self.raw).bind(
                    lambda conf_2: unfolder.get_required("locations")
                    .map(Unfolder)
                    .bind(lambda u: u.to_list_of(str).alt(Exception))
                    .bind(
                        lambda locations: unfolder.require_primitive(
                            "created_at", str
                        )
                        .bind(isoparse)
                        .bind(
                            lambda created_at: unfolder.require_primitive(
                                "update_at", str
                            )
                            .bind(isoparse)
                            .map(
                                lambda updated_at: Check(
                                    name,
                                    conf_1,
                                    conf_2,
                                    locations,
                                    created_at,
                                    updated_at,
                                )
                            )
                        )
                    )
                )
            )
        )

    def decode_id(self) -> ResultE[CheckId]:
        unfolder = ExtendedUnfolder(self.raw)
        return unfolder.require_primitive("id", str).map(CheckId)

    def decode_obj(self) -> ResultE[CheckObj]:
        return self.decode_id().bind(
            lambda cid: self.decode_check().map(lambda c: IndexedObj(cid, c))
        )
