# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class Source(str, Enum):
    ANALYST: str = "ANALYST"
    ASM: str = "ASM"
    CUSTOMER: str = "CUSTOMER"
    DETERMINISTIC: str = "DETERMINISTIC"
    ESCAPE: str = "ESCAPE"
    MACHINE: str = "MACHINE"


class StateRemovalJustification(str, Enum):
    DUPLICATED: str = "DUPLICATED"
    EXCLUSION: str = "EXCLUSION"
    FALSE_POSITIVE: str = "FALSE_POSITIVE"
    NO_JUSTIFICATION: str = "NO_JUSTIFICATION"
    NOT_REQUIRED: str = "NOT_REQUIRED"
    REPORTING_ERROR: str = "REPORTING_ERROR"


class CredentialType(str, Enum):
    SSH: str = "SSH"
    HTTPS: str = "HTTPS"


class GitCloningStatus(str, Enum):
    CLONING: str = "CLONING"
    FAILED: str = "FAILED"
    OK: str = "OK"
    QUEUED: str = "QUEUED"
    UNKNOWN: str = "UNKNOWN"


class Notification(str, Enum):
    ACCESS_GRANTED: str = "ACCESS_GRANTED"
    AGENT_TOKEN: str = "AGENT_TOKEN"
    CHARTS_REPORT: str = "CHARTS_REPORT"
    EVENT_REPORT: str = "EVENT_REPORT"
    FILE_UPDATE: str = "FILE_UPDATE"
    GROUP_INFORMATION: str = "GROUP_INFORMATION"
    GROUP_REPORT: str = "GROUP_REPORT"
    NEW_COMMENT: str = "NEW_COMMENT"
    NEW_DRAFT: str = "NEW_DRAFT"
    PORTFOLIO_UPDATE: str = "PORTFOLIO_UPDATE"
    REMEDIATE_FINDING: str = "REMEDIATE_FINDING"
    REMINDER_NOTIFICATION: str = "REMINDER_NOTIFICATION"
    ROOT_UPDATE: str = "ROOT_UPDATE"
    SERVICE_UPDATE: str = "SERVICE_UPDATE"
    UNSUBSCRIPTION_ALERT: str = "UNSUBSCRIPTION_ALERT"
    UPDATED_TREATMENT: str = "UPDATED_TREATMENT"
    VULNERABILITY_ASSIGNED: str = "VULNERABILITY_ASSIGNED"
    VULNERABILITY_REPORT: str = "VULNERABILITY_REPORT"
