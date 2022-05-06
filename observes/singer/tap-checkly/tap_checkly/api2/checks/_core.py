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
class Check:
    name: str
    activated: bool
    muted: bool
    double_check: bool
    ssl_check: bool
    should_fail: bool
    locations: FrozenList[str]
    use_global_alert_settings: bool
    group_id: CheckGroupId
    group_order: int
    runtime_ver: str
    check_type: str
    frequency: int
    frequency_offset: int
    degraded_response_time: int
    max_response_time: int
    created_at: datetime
    updated_at: datetime


CheckObj = IndexedObj[CheckId, Check]
__all__ = [
    "CheckId",
]
