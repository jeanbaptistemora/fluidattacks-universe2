from .enums import (
    FindingStateJustification,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from .types import (
    FindingEvidences,
    FindingState,
    FindingUnreliableIndicators,
    FindingVerification,
)
from db_model.enums import (
    Source,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Optional,
)


def format_evidences_item(evidences: FindingEvidences) -> Item:
    return {
        field: evidence._asdict()
        for field, evidence in evidences._asdict().items()
        if evidence is not None
    }


def format_state(state_item: Item) -> FindingState:
    return FindingState(
        justification=FindingStateJustification[state_item["justification"]],
        modified_by=state_item["modified_by"],
        modified_date=state_item["modified_date"],
        source=Source[state_item["source"]],
        status=FindingStateStatus[state_item["status"]],
    )


def format_state_item(state: FindingState) -> Item:
    return {
        "justification": state.justification.value,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "source": state.source.value,
        "status": state.status.value,
    }


def format_unreliable_indicators_item(
    indicators: FindingUnreliableIndicators,
) -> Item:
    return {
        "unreliable_age": indicators.unreliable_age,
        "unreliable_closed_vulnerabilities": (
            indicators.unreliable_closed_vulnerabilities
        ),
        "unreliable_is_verified": indicators.unreliable_is_verified,
        "unreliable_last_vulnerability": (
            indicators.unreliable_last_vulnerability
        ),
        "unreliable_open_age": indicators.unreliable_open_age,
        "unreliable_open_vulnerabilities": (
            indicators.unreliable_open_vulnerabilities
        ),
        "unreliable_report_date": indicators.unreliable_report_date,
        "unreliable_status": indicators.unreliable_status.value,
    }


def format_unreliable_indicators(
    indicators_item: Item,
) -> FindingUnreliableIndicators:
    return FindingUnreliableIndicators(
        unreliable_age=indicators_item["unreliable_age"],
        unreliable_closed_vulnerabilities=(
            indicators_item["unreliable_closed_vulnerabilities"]
        ),
        unreliable_is_verified=indicators_item["unreliable_is_verified"],
        unreliable_last_vulnerability=(
            indicators_item["unreliable_last_vulnerability"]
        ),
        unreliable_open_age=indicators_item["unreliable_open_age"],
        unreliable_open_vulnerabilities=(
            indicators_item["unreliable_open_vulnerabilities"]
        ),
        unreliable_report_date=indicators_item["unreliable_report_date"],
        unreliable_status=FindingStatus[indicators_item["unreliable_status"]],
    )


def format_verification(verification_item: Item) -> FindingVerification:
    return FindingVerification(
        comment_id=verification_item["comment_id"],
        modified_by=verification_item["modified_by"],
        modified_date=verification_item["modified_date"],
        status=FindingVerificationStatus[verification_item["status"]],
        vuln_uuids=verification_item["vuln_uuids"],
    )


def format_verification_item(verification: FindingVerification) -> Item:
    return {
        "comment_id": verification.comment_id,
        "modified_by": verification.modified_by,
        "modified_date": verification.modified_date,
        "status": verification.status.value,
        "vuln_uuids": verification.vuln_uuids,
    }


def format_optional_verification(
    verification_item: Item,
) -> Optional[FindingVerification]:
    verification = None
    if verification_item.get("status"):
        verification = format_verification(verification_item)
    return verification


def format_optional_verification_item(
    verification: Optional[FindingVerification],
) -> Item:
    verification_item = {}
    if verification is not None:
        verification_item = format_verification_item(verification)
    return verification_item
