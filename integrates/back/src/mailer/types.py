from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class TrialEngagementInfo(NamedTuple):
    email_to: str
    group_name: str
    start_date: datetime
