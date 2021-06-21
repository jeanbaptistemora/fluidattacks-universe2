from db_model.enums import (
    Source,
)
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


class VulnerabilityDeletionJustification(Enum):
    DUPLICATED: str = "DUPLICATED"
    FALSE_POSITIVE: str = "FALSE_POSITIVE"
    REPORTING_ERROR: str = "REPORTING_ERROR"
    NO_JUSTIFICATION: str = "NO_JUSTIFICATION"


class VulnerabilityApprovalStatus(Enum):
    APPROVED: str = "APPROVED"
    PENDING: str = "PENDING"


class VulnerabilityStatus(Enum):
    CLOSED: str = "CLOSED"
    DELETED: str = "DELETED"
    OPEN: str = "OPEN"


class VulnerabilityState(NamedTuple):
    approval_status: Optional[VulnerabilityApprovalStatus]
    justification: Optional[VulnerabilityDeletionJustification]
    modified_by: str
    modified_date: str
    source: Source
    status: VulnerabilityStatus


def format_state(item: Item) -> VulnerabilityState:
    return VulnerabilityState(
        approval_status=VulnerabilityApprovalStatus[item["approval_status"]]
        if "approval_status" in item
        else None,
        justification=VulnerabilityDeletionJustification[item["justification"]]
        if "justification" in item
        else None,
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        source=Source[item["source"]],
        status=VulnerabilityStatus[item["status"]],
    )


def format_state_item(state: VulnerabilityState) -> Item:
    return {
        "approval_status": state.approval_status.value
        if state.approval_status
        else None,
        "justification": state.justification.value
        if state.justification
        else None,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "source": state.source.value,
        "status": state.status.value,
    }
