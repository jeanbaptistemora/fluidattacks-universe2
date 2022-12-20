from ariadne import (
    EnumType,
)
from typing import (
    Tuple,
)

ENUMS: Tuple[EnumType, ...] = (
    EnumType(
        "AffectedComponents",
        {
            "TEST_DATA": "TEST_DATA",
            "TOE_CREDENTIALS": "TOE_CREDENTIALS",
            "TOE_PRIVILEGES": "TOE_PRIVILEGES",
            "TOE_UNAVAILABLE": "TOE_UNAVAILABLE",
            "TOE_UNSTABLE": "TOE_UNSTABLE",
        },
    ),
    EnumType(
        "BillingSubscriptionType",
        {
            "FREE": "free",
            "MACHINE": "machine",
            "SQUAD": "squad",
        },
    ),
    EnumType("CallerOrigin", {"API": "API", "FRONT": "FRONT"}),
    EnumType(
        "DraftRejectionReason",
        {
            "CONSISTENCY": "CONSISTENCY",
            "EVIDENCE": "EVIDENCE",
            "NAMING": "NAMING",
            "OMISSION": "OMISSION",
            "OTHER": "OTHER",
            "SCORING": "SCORING",
            "WRITING": "WRITING",
        },
    ),
    EnumType(
        "RemoveFindingJustification",
        {
            "DUPLICATED": "DUPLICATED",
            "FALSE_POSITIVE": "FALSE_POSITIVE",
            "NOT_REQUIRED": "NOT_REQUIRED",
        },
    ),
    EnumType(
        "RemoveVulnerabilityJustification",
        {
            "DUPLICATED": "DUPLICATED",
            "FALSE_POSITIVE": "FALSE_POSITIVE",
            "REPORTING_ERROR": "REPORTING_ERROR",
        },
    ),
    EnumType(
        "UpdateGroupReason",
        {
            "BUDGET": "BUDGET",
            "NONE": "NONE",
            "OTHER": "OTHER",
            "GROUP_FINALIZATION": "GROUP_FINALIZATION",
            "GROUP_SUSPENSION": "GROUP_SUSPENSION",
        },
    ),
    EnumType(
        "EventAccessibility",
        {
            "ENVIRONMENT": "ENVIRONMENT",
            "REPOSITORY": "REPOSITORY",
            "VPN_CONNECTION": "VPN_CONNECTION",
        },
    ),
    EnumType(
        "SolveEventReason",
        {
            "ACCESS_GRANTED": "ACCESS_GRANTED",
            "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE": (
                "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE"
            ),
            "CLONED_SUCCESSFULLY": "CLONED_SUCCESSFULLY",
            "CREDENTIALS_ARE_WORKING_NOW": "CREDENTIALS_ARE_WORKING_NOW",
            "DATA_UPDATED": "DATA_UPDATED",
            "ENVIRONMENT_IS_WORKING_NOW": "ENVIRONMENT_IS_WORKING_NOW",
            "INSTALLER_IS_WORKING_NOW": "INSTALLER_IS_WORKING_NOW",
            "IS_OK_TO_RESUME": "IS_OK_TO_RESUME",
            "NEW_CREDENTIALS_PROVIDED": "NEW_CREDENTIALS_PROVIDED",
            "NEW_ENVIRONMENT_PROVIDED": "NEW_ENVIRONMENT_PROVIDED",
            "OTHER": "OTHER",
            "PERMISSION_DENIED": "PERMISSION_DENIED",
            "PERMISSION_GRANTED": "PERMISSION_GRANTED",
            "PROBLEM_SOLVED": "PROBLEM_SOLVED",
            "SUPPLIES_WERE_GIVEN": "SUPPLIES_WERE_GIVEN",
            "TOE_CHANGE_APPROVED": "TOE_CHANGE_APPROVED",
            "TOE_WILL_REMAIN_UNCHANGED": "TOE_WILL_REMAIN_UNCHANGED",
        },
    ),
    EnumType(
        "EventEvidenceType",
        {
            "FILE_1": "FILE_1",
            "IMAGE_1": "IMAGE_1",
            "IMAGE_2": "IMAGE_2",
            "IMAGE_3": "IMAGE_3",
            "IMAGE_4": "IMAGE_4",
            "IMAGE_5": "IMAGE_5",
            "IMAGE_6": "IMAGE_6",
        },
    ),
    EnumType(
        "EventType",
        {
            "AUTHORIZATION_SPECIAL_ATTACK": "AUTHORIZATION_SPECIAL_ATTACK",
            "CLIENT_CANCELS_PROJECT_MILESTONE": (
                "CLIENT_CANCELS_PROJECT_MILESTONE"
            ),
            "CLIENT_EXPLICITLY_SUSPENDS_PROJECT": (
                "CLIENT_EXPLICITLY_SUSPENDS_PROJECT"
            ),
            "CLONING_ISSUES": "CLONING_ISSUES",
            "CREDENTIAL_ISSUES": "CREDENTIAL_ISSUES",
            "DATA_UPDATE_REQUIRED": "DATA_UPDATE_REQUIRED",
            "ENVIRONMENT_ISSUES": "ENVIRONMENT_ISSUES",
            "INSTALLER_ISSUES": "INSTALLER_ISSUES",
            "INCORRECT_MISSING_SUPPLIES": "INCORRECT_MISSING_SUPPLIES",
            "MISSING_SUPPLIES": "MISSING_SUPPLIES",
            "NETWORK_ACCESS_ISSUES": "NETWORK_ACCESS_ISSUES",
            "OTHER": "OTHER",
            "REMOTE_ACCESS_ISSUES": "REMOTE_ACCESS_ISSUES",
            "TOE_DIFFERS_APPROVED": "TOE_DIFFERS_APPROVED",
            "VPN_ISSUES": "VPN_ISSUES",
        },
    ),
    EnumType(
        "EvidenceDescriptionType",
        {
            "ANIMATION": "animation",
            "EVIDENCE1": "evidence_route_1",
            "EVIDENCE2": "evidence_route_2",
            "EVIDENCE3": "evidence_route_3",
            "EVIDENCE4": "evidence_route_4",
            "EVIDENCE5": "evidence_route_5",
            "EXPLOITATION": "exploitation",
        },
    ),
    EnumType(
        "EvidenceType",
        {
            "ANIMATION": "animation",
            "EVIDENCE1": "evidence_route_1",
            "EVIDENCE2": "evidence_route_2",
            "EVIDENCE3": "evidence_route_3",
            "EVIDENCE4": "evidence_route_4",
            "EVIDENCE5": "evidence_route_5",
            "EXPLOITATION": "exploitation",
            "RECORDS": "fileRecords",
        },
    ),
    EnumType(
        "FindingConsultType",
        {"CONSULT": "CONSULT", "OBSERVATION": "OBSERVATION"},
    ),
    EnumType(
        "Frequency",
        {
            "DAILY": "DAILY",
            "HOURLY": "HOURLY",
            "MONTHLY": "MONTHLY",
            "NEVER": "NEVER",
            "WEEKLY": "WEEKLY",
        },
    ),
    EnumType("Language", {"EN": "EN", "ES": "ES"}),
    EnumType(
        "ManagedType",
        {
            "MANAGED": "MANAGED",
            "NOT_MANAGED": "NOT_MANAGED",
            "UNDER_REVIEW": "UNDER_REVIEW",
            "TRIAL": "TRIAL",
        },
    ),
    EnumType(
        "EnrollmentTrialState",
        {
            "EXTENDED": "EXTENDED",
            "EXTENDED_ENDED": "EXTENDED_ENDED",
            "TRIAL": "TRIAL",
            "TRIAL_ENDED": "TRIAL_ENDED",
        },
    ),
    EnumType(
        "OrganizationFindingPolicy",
        {"APPROVED": "APPROVED", "REJECTED": "REJECTED"},
    ),
    EnumType(
        "OrganizationRole",
        {
            "CUSTOMER_MANAGER": "CUSTOMER_MANAGER",
            "USER": "USER",
            "USER_MANAGER": "USER_MANAGER",
        },
    ),
    EnumType("ReportLang", {"EN": "en"}),
    EnumType(
        "ReportType",
        {"CERT": "CERT", "DATA": "DATA", "PDF": "PDF", "XLS": "XLS"},
    ),
    EnumType("ResourceState", {"ACTIVE": "ACTIVE", "INACTIVE": "INACTIVE"}),
    EnumType("ServiceType", {"BLACK": "BLACK", "WHITE": "WHITE"}),
    EnumType("Sorts", {"NO": "NO", "YES": "YES"}),
    EnumType(
        "StakeholderEntity",
        {"ORGANIZATION": "ORGANIZATION", "GROUP": "GROUP"},
    ),
    EnumType(
        "StakeholderRole",
        {
            "ADMIN": "admin",
            "ARCHITECT": "architect",
            "CUSTOMER_MANAGER": "customer_manager",
            "HACKER": "hacker",
            "REATTACKER": "reattacker",
            "RESOURCER": "resourcer",
            "REVIEWER": "reviewer",
            "SERVICE_FORCES": "service_forces",
            "USER": "user",
            "USER_MANAGER": "user_manager",
            "VULNERABILITY_MANAGER": "vulnerability_manager",
        },
    ),
    EnumType(
        "SubscriptionReportEntity",
        {
            "GROUP": "GROUP",
            "ORGANIZATION": "ORGANIZATION",
            "PORTFOLIO": "PORTFOLIO",
        },
    ),
    EnumType(
        "SubscriptionType", {"CONTINUOUS": "continuous", "ONESHOT": "oneshot"}
    ),
    EnumType(
        "TierType",
        {
            "FREE": "FREE",
            "MACHINE": "MACHINE",
            "ONESHOT": "ONESHOT",
            "OTHER": "OTHER",
            "SQUAD": "SQUAD",
        },
    ),
    EnumType(
        "UpdateClientDescriptionTreatment",
        {
            "ACCEPTED": "ACCEPTED",
            "ACCEPTED_UNDEFINED": "ACCEPTED_UNDEFINED",
            "IN_PROGRESS": "IN PROGRESS",
        },
    ),
    EnumType(
        "VulnerabilitySource",
        {
            "ANALYST": "ANALYST",
            "CUSTOMER": "CUSTOMER",
            "DETERMINISTIC": "DETERMINISTIC",
            "ESCAPE": "ESCAPE",
            "MACHINE": "MACHINE",
        },
    ),
    EnumType(
        "VulnerabilityState",
        {
            "CLOSED": "CLOSED",
            "OPEN": "OPEN",
            "SAFE": "SAFE",
            "VULNERABLE": "VULNERABLE",
        },
    ),
    EnumType(
        "VulnerabilityVerification",
        {
            "REQUESTED": "REQUESTED",
            "ON_HOLD": "ON_HOLD",
            "VERIFIED": "VERIFIED",
        },
    ),
    EnumType(
        "VulnerabilityExploitState",
        {
            "ACCEPTED": "ACCEPTED",
            "CLOSED": "CLOSED",
            "OPEN": "OPEN",
            "UNKNOWN": "UNKNOWN",
        },
    ),
)
