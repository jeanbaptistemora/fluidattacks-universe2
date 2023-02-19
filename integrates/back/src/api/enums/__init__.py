from ariadne import (
    EnumType,
)

# Note: by default, enum values are the same as their name
# Only declare them here if you need to map the value to something else
# https://ariadnegraphql.org/docs/enums#mapping-to-internal-values

ENUMS: tuple[EnumType, ...] = (
    EnumType(
        "BillingSubscriptionType",
        {
            "FREE": "free",
            "MACHINE": "machine",
            "SQUAD": "squad",
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
    EnumType("ReportLang", {"EN": "en"}),
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
        "SubscriptionType", {"CONTINUOUS": "continuous", "ONESHOT": "oneshot"}
    ),
    EnumType(
        "UpdateClientDescriptionTreatment",
        {
            "ACCEPTED": "ACCEPTED",
            "ACCEPTED_UNDEFINED": "ACCEPTED_UNDEFINED",
            "IN_PROGRESS": "IN PROGRESS",
        },
    ),
)
