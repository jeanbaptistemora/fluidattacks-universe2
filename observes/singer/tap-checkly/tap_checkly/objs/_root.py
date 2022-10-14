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
from ._group import (
    CheckGroup,
    CheckId,
)
from ._id_objs import (
    IndexedObj,
)
from ._result import (
    CheckResult,
    CheckResultId,
)
from ._subscriptions import (
    AlertChannelId,
)
from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class CheckGroupId:
    id_str: str


CheckStatusObj = IndexedObj[CheckId, CheckStatus]
CheckObj = IndexedObj[CheckId, Check]
AlertChannelObj = IndexedObj[AlertChannelId, AlertChannel]
CheckResultObj = IndexedObj[CheckResultId, CheckResult]
CheckGroupObj = IndexedObj[CheckGroupId, CheckGroup]
