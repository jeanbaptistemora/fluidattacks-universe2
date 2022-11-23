from enum import (
    Enum,
)


class SupportedStreams(Enum):
    ALERT_CHS = "ALERT_CHS"
    CHECKS = "CHECKS"
    CHECK_GROUPS = "CHECK_GROUPS"
    CHECK_RESULTS = "CHECK_RESULTS"
    CHECK_STATUS = "CHECK_STATUS"
    REPORTS = "REPORTS"
