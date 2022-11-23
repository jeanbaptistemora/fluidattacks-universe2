from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Maybe,
)


@dataclass(frozen=True)
class AlertChannel:
    alert_type: str
    send_recovery: bool
    send_failure: bool
    send_degraded: bool
    ssl_expiry: bool
    ssl_expiry_threshold: int
    created_at: datetime
    updated_at: Maybe[datetime]
