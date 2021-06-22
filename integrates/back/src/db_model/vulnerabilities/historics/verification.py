from dynamodb.types import (
    Item,
)
from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)


class VulnerabilityVerificationStatus(Enum):
    REQUESTED: str = "REQUESTED"
    VERIFIED: str = "VERIFIED"


class VulnerabilityVerification(NamedTuple):
    modified_by: str
    modified_date: str
    status: VulnerabilityVerificationStatus


def format_verification(item: Item) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=VulnerabilityVerificationStatus[item["status"]],
    )


def format_verification_item(state: VulnerabilityVerification) -> Item:
    return {
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }
