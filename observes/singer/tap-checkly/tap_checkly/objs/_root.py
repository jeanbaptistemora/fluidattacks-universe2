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
    DateRange,
    IndexedObj,
)
from ._report import (
    CheckReport,
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
from typing import (
    Tuple,
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


# objs paired with its own full id obj
CheckStatusObj = IndexedObj[CheckId, CheckStatus]
CheckObj = IndexedObj[CheckId, Check]
AlertChannelObj = IndexedObj[AlertChannelId, AlertChannel]
CheckResultObj = IndexedObj[Tuple[CheckId, CheckResultId], CheckResult]
CheckGroupObj = IndexedObj[CheckGroupId, CheckGroup]
DashboardObj = IndexedObj[DashboardId, Dashboard]
ReportObj = IndexedObj[DateRange, CheckReport]
