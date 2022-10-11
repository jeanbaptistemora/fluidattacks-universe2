# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenList,
)
from tap_checkly.api2.id_objs import (
    CheckGroupId,
    CheckId,
    IndexedObj,
)


@dataclass(frozen=True)
class CheckConf1:
    activated: bool
    muted: bool
    double_check: bool
    ssl_check: bool
    should_fail: bool
    use_global_alert_settings: bool


@dataclass(frozen=True)
class CheckConf2:
    group_id: CheckGroupId
    group_order: int
    runtime_ver: str
    check_type: str
    frequency: int
    frequency_offset: int
    degraded_response_time: int
    max_response_time: int


@dataclass(frozen=True)
class Check:
    name: str
    conf_1: CheckConf1
    conf_2: CheckConf2
    locations: FrozenList[str]
    created_at: datetime
    updated_at: datetime


CheckObj = IndexedObj[CheckId, Check]
__all__ = [
    "CheckId",
]
