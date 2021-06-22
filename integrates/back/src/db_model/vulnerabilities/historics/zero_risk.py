from dynamodb.types import (
    Item,
)
from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)


class VulnerabilityZeroRiskStatus(Enum):
    CONFIRMED: str = "CONFIRMED"
    REJECTED: str = "REJECTED"
    REQUESTED: str = "REQUESTED"


class VulnerabilityZeroRisk(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: str
    status: VulnerabilityZeroRiskStatus


def format_zero_risk(item: Item) -> VulnerabilityZeroRisk:
    return VulnerabilityZeroRisk(
        comment_id=item["comment_id"],
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=VulnerabilityZeroRiskStatus[item["status"]],
    )


def format_zero_risk_item(state: VulnerabilityZeroRisk) -> Item:
    return {
        "comment_id": state.comment_id,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }
