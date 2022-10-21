# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._alert import (
    AlertChannel,
)
from ._check import (
    Check,
    CheckStatus,
)
from ._dashboard import (
    Dashboard,
)
from ._group import (
    CheckGroup,
    CheckId,
)
from ._id_objs import (
    IndexedObj,
)
from ._subscriptions import (
    AlertChannelId,
)
from .result import (
    CheckResult,
)
from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class CheckResultId:
    id_str: str


@dataclass(frozen=True)
class CheckGroupId:
    raw_id: int


@dataclass(frozen=True)
class DashboardId:
    raw_id: str


CheckStatusObj = IndexedObj[CheckId, CheckStatus]
CheckObj = IndexedObj[CheckId, Check]
AlertChannelObj = IndexedObj[AlertChannelId, AlertChannel]
CheckResultObj = IndexedObj[CheckResultId, CheckResult]
CheckGroupObj = IndexedObj[CheckGroupId, CheckGroup]
DashboardObj = IndexedObj[DashboardId, Dashboard]
