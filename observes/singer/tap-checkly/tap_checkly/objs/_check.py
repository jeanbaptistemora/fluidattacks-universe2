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
    Maybe,
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


@dataclass(frozen=True)
class CheckStatus:
    name: str
    created_at: datetime
    has_errors: bool
    has_failures: bool
    is_degraded: bool
    last_check_run_id: str
    last_run_location: str
    longest_run: int
    shortest_run: int
    ssl_days_remaining: int
    updated_at: Maybe[datetime]
