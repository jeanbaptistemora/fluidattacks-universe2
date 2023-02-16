from enum import (
    Enum,
)


class MailVulnerabilityReportState(str, Enum):
    REPORTED: str = "REPORTED"
    SOLVED: str = "SOLVED"
    SUBMITTED: str = "SUBMITTED"
