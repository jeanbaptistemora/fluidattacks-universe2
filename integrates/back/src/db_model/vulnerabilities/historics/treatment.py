from dynamodb.types import (
    Item,
)
from enum import (
    Enum,
)
from typing import (
    NamedTuple,
    Optional,
)


class VulnerabilityTreatmentStatus(Enum):
    ACCEPTED: str = "ACCEPTED"
    ACCEPTED_UNDEFINED: str = "ACCEPTED_UNDEFINED"
    IN_PROGRESS: str = "IN_PROGRESS"
    NEW: str = "NEW"


class VulnerabilityAcceptanceStatus(Enum):
    APPROVED: str = "APPROVED"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"


class VulnerabilityTreatment(NamedTuple):
    accepted_until: Optional[str]
    acceptance_status: Optional[VulnerabilityAcceptanceStatus]
    justification: Optional[str]
    manager: Optional[str]
    modified_by: str
    modified_date: str
    status: VulnerabilityTreatmentStatus


def format_treatment(item: Item) -> VulnerabilityTreatment:
    return VulnerabilityTreatment(
        accepted_until=item.get("accepted_until", None),
        acceptance_status=VulnerabilityAcceptanceStatus[
            item["acceptance_status"]
        ]
        if "acceptance_status" in item
        else None,
        justification=item.get("justification", None),
        manager=item.get("manager", None),
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=VulnerabilityTreatmentStatus[item["status"]],
    )


def format_treatment_item(state: VulnerabilityTreatment) -> Item:
    return {
        "accepted_until": state.accepted_until,
        "acceptance_status": state.acceptance_status.value
        if state.acceptance_status
        else None,
        "justification": state.justification,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }
