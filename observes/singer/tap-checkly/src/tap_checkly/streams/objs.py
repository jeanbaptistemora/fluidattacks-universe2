from enum import (
    Enum,
)


class SupportedStreams(Enum):
    ALERT_CHS = "ALERT_CHS"
    CHECKS = "CHECKS"
    CHECK_GROUPS = "CHECK_GROUPS"
    CHECK_RESULTS = "CHECK_RESULTS"  # rolled up results deprecated from source
    CHECK_STATUS = "CHECK_STATUS"
    DASHBOARD = "DASHBOARD"
    ENV_VARS = "ENV_VARS"
    MAINTENACE_WINDOWS = "MAINTENACE_WINDOWS"
    REPORTS = "REPORTS"
    SNIPPETS = "SNIPPETS"
