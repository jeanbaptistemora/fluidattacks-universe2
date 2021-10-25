from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityDeletionJustification,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from .types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from db_model import (
    TABLE,
)
from db_model.enums import (
    Source,
)
from dynamodb import (
    historics,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from typing import (
    Optional,
    Tuple,
)


def format_vulnerability(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> Vulnerability:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    inverted_index = TABLE.indexes["inverted_index"]
    inverted_key_structure = inverted_index.primary_key
    metadata["finding_id"] = metadata[
        inverted_key_structure.partition_key
    ].split("#")[1]
    metadata["id"] = metadata[inverted_key_structure.sort_key].split("#")[1]

    state: VulnerabilityState = format_state(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="STATE",
            raw_items=raw_items,
        )
    )

    treatment: VulnerabilityTreatment = format_treatment(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="TREATMENT",
            raw_items=raw_items,
        )
    )

    try:
        verification: Optional[
            VulnerabilityVerification
        ] = format_verification(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="VERIFICATION",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        verification = None

    try:
        zero_risk: Optional[VulnerabilityZeroRisk] = format_zero_risk(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="ZERORISK",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        zero_risk = None

    return Vulnerability(
        bug_tracking_system_url=metadata.get("bug_tracking_system_url", None),
        commit=metadata.get("commit", None),
        custom_severity=metadata.get("custom_severity", None),
        finding_id=metadata["finding_id"],
        hash=metadata.get("hash", None),
        repo=metadata.get("repo", None),
        specific=metadata["specific"],
        state=state,
        stream=metadata.get("stream", None),
        tags=metadata.get("tags", None),
        treatment=treatment,
        type=VulnerabilityType[metadata["type"]],
        id=metadata["id"],
        verification=verification,
        where=metadata["where"],
        zero_risk=zero_risk,
    )


def format_state(item: Item) -> VulnerabilityState:
    return VulnerabilityState(
        justification=VulnerabilityDeletionJustification[item["justification"]]
        if item.get("justification", None)
        else None,
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        source=Source[item["source"]],
        status=VulnerabilityStateStatus[item["status"]],
    )


def format_state_item(state: VulnerabilityState) -> Item:
    return {
        "justification": state.justification.value
        if state.justification
        else None,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "source": state.source.value,
        "status": state.status.value,
    }


def format_treatment(item: Item) -> VulnerabilityTreatment:
    return VulnerabilityTreatment(
        accepted_until=item.get("accepted_until", None),
        acceptance_status=VulnerabilityAcceptanceStatus[
            item["acceptance_status"]
        ]
        if item.get("acceptance_status", None)
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
        "manager": state.manager,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }


def format_verification(item: Item) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        comment_id=item["comment_id"],
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=VulnerabilityVerificationStatus[item["status"]],
    )


def format_verification_item(state: VulnerabilityVerification) -> Item:
    return {
        "comment_id": state.comment_id,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }


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
