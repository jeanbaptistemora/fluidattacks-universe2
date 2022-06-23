from ariadne import (
    EnumType,
)
from typing import (
    Tuple,
)

ENUMS: Tuple[EnumType, ...] = (
    EnumType(
        "ActionsAfterBlocking",
        {
            "EXECUTE_OTHER_GROUP_OTHER_CLIENT": (
                "EXECUTE_OTHER_GROUP_OTHER_CLIENT"
            ),
            "EXECUTE_OTHER_GROUP_SAME_CLIENT": (
                "EXECUTE_OTHER_GROUP_SAME_CLIENT"
            ),
            "NONE": "NONE",
            "OTHER": "OTHER",
            "TRAINING": "TRAINING",
        },
    ),
    EnumType(
        "ActionsBeforeBlocking",
        {
            "DOCUMENT_GROUP": "DOCUMENT_GROUP",
            "NONE": "NONE",
            "OTHER": "OTHER",
            "TEST_OTHER_PART_TOE": "TEST_OTHER_PART_TOE",
        },
    ),
    EnumType(
        "AffectedComponents",
        {
            "CLIENT_STATION": "CLIENT_STATION",
            "COMPILE_ERROR": "COMPILE_ERROR",
            "DOCUMENTATION": "DOCUMENTATION",
            "FLUID_STATION": "FLUID_STATION",
            "INTERNET_CONNECTION": "INTERNET_CONNECTION",
            "LOCAL_CONNECTION": "LOCAL_CONNECTION",
            "OTHER": "OTHER",
            "SOURCE_CODE": "SOURCE_CODE",
            "TEST_DATA": "TEST_DATA",
            "TOE_ALTERATION": "TOE_ALTERATION",
            "TOE_CREDENTIALS": "TOE_CREDENTIALS",
            "TOE_EXCLUSSION": "TOE_EXCLUSSION",
            "TOE_LOCATION": "TOE_LOCATION",
            "TOE_PRIVILEGES": "TOE_PRIVILEGES",
            "TOE_UNACCESSIBLE": "TOE_UNACCESSIBLE",
            "TOE_UNAVAILABLE": "TOE_UNAVAILABLE",
            "TOE_UNSTABLE": "TOE_UNSTABLE",
            "VPN_CONNECTION": "VPN_CONNECTION",
        },
    ),
    EnumType(
        "AuthProvider",
        {
            "BITBUCKET": "bitbucket",
            "GOOGLE": "google",
            "MICROSOFT": "microsoft",
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
            "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE": (
                "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE"
            ),
            "OTHER": "OTHER",
            "PERMISSION_DENIED": "PERMISSION_DENIED",
            "PERMISSION_GRANTED": "PERMISSION_GRANTED",
            "PROBLEM_SOLVED": "PROBLEM_SOLVED",
            "SUPPLIES_WERE_GIVEN": "SUPPLIES_WERE_GIVEN",
            "TOE_CHANGE_APPROVED": "TOE_CHANGE_APPROVED",
            "TOE_WILL_REMAIN_UNCHANGED": "TOE_WILL_REMAIN_UNCHANGED",
        },
    ),
    EnumType("EventEvidenceType", {"FILE": "FILE", "IMAGE": "IMAGE"}),
    EnumType(
        "EventType",
        {
            "AUTHORIZATION_SPECIAL_ATTACK": "AUTHORIZATION_SPECIAL_ATTACK",
            "DATA_UPDATE_REQUIRED": "DATA_UPDATE_REQUIRED",
            "INCORRECT_MISSING_SUPPLIES": "INCORRECT_MISSING_SUPPLIES",
            "OTHER": "OTHER",
            "TOE_DIFFERS_APPROVED": "TOE_DIFFERS_APPROVED",
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
        "OrganizationFindingPolicy",
        {"APPROVED": "APPROVED", "REJECTED": "REJECTED"},
    ),
    EnumType(
        "OrganizationRole",
        {
            "CUSTOMER": "CUSTOMER",
            "CUSTOMER_MANAGER": "CUSTOMER_MANAGER",
            "CUSTOMERADMIN": "CUSTOMERADMIN",
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
            "CUSTOMER": "customer",
            "CUSTOMER_MANAGER": "customer_manager",
            "CUSTOMERADMIN": "customeradmin",
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
            "COMMENTS": "COMMENTS",
            "DIGEST": "DIGEST",
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
            "FREE": "free",
            "MACHINE": "machine",
            "ONESHOT": "oneshot",
            "OTHER": "other",
            "SQUAD": "squad",
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
        "VulnerabilityState",
        {
            "CLOSED": "CLOSED",
            "OPEN": "OPEN",
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
