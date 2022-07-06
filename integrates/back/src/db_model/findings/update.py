from .enums import (
    FindingCvssVersion,
    FindingEvidenceName,
    FindingStateStatus,
)
from .types import (
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingEvidenceToUpdate,
    FindingMetadataToUpdate,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
    FindingVerificationSummary,
)
from .utils import (
    format_evidences_item,
    format_state_item,
    format_treatment_summary_item,
    format_unreliable_indicators_item,
    format_verification_item,
    format_verification_summary_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    FindingNotFound,
    IndicatorAlreadyUpdated,
)
from db_model import (
    TABLE,
)
from db_model.findings.constants import (
    ME_DRAFTS_INDEX_METADATA,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from enum import (
    Enum,
)
from typing import (
    Optional,
)


async def update_evidence(
    *,
    current_value: FindingEvidence,
    evidence_name: FindingEvidenceName,
    evidence: FindingEvidenceToUpdate,
    finding_id: str,
    group_name: str,
) -> None:
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    attribute = f"evidences.{evidence_name.value}"
    await operations.update_item(
        condition_expression=Attr(attribute).eq(current_value._asdict()),
        item={
            f"{attribute}.{key}": value
            for key, value in evidence._asdict().items()
            if value is not None
        },
        key=metadata_key,
        table=TABLE,
    )


async def update_me_draft_index(
    *,
    finding_id: str,
    group_name: str,
    user_email: str,
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]

    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    base_condition = Attr(key_structure.partition_key).exists()
    gsi_2_key = keys.build_key(
        facet=ME_DRAFTS_INDEX_METADATA,
        values={
            "email": user_email,
            "id": finding_id,
        },
    )
    vulnerability_item = {
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
    }
    await operations.update_item(
        condition_expression=(base_condition),
        item=vulnerability_item,
        key=metadata_key,
        table=TABLE,
    )


async def update_metadata(
    *,
    group_name: str,
    finding_id: str,
    metadata: FindingMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    metadata_item = {
        key: value.value
        if isinstance(value, Enum)
        else value._asdict()
        if isinstance(value, (Finding20Severity, Finding31Severity))
        else format_evidences_item(value)
        if isinstance(value, FindingEvidences)
        else value
        for key, value in metadata._asdict().items()
        if value is not None
    }
    if "severity" in metadata_item:
        cvss_version = (
            FindingCvssVersion.V31
            if isinstance(metadata.severity, Finding31Severity)
            else FindingCvssVersion.V20
        )
        metadata_item["cvss_version"] = cvss_version.value
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )


async def update_state(  # pylint: disable=too-many-locals
    *,
    current_value: FindingState,
    finding_id: str,
    group_name: str,
    state: FindingState,
) -> None:
    items = []
    key_structure = TABLE.primary_key
    state_item = format_state_item(state)
    latest, historic = historics.build_historic(
        attributes=state_item,
        historic_facet=TABLE.facets["finding_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "group_name": group_name,
            "id": finding_id,
        },
        latest_facet=TABLE.facets["finding_state"],
    )
    try:
        await operations.put_item(
            condition_expression=(
                Attr("status").ne(FindingStateStatus.DELETED.value)
                & Attr("modified_date").eq(current_value.modified_date)
            ),
            facet=TABLE.facets["finding_state"],
            item=latest,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise FindingNotFound() from ex
    items.append(historic)
    if state.status == FindingStateStatus.APPROVED:
        approval_key = keys.build_key(
            facet=TABLE.facets["finding_approval"],
            values={"group_name": group_name, "id": finding_id},
        )
        approval = {
            key_structure.partition_key: approval_key.partition_key,
            key_structure.sort_key: approval_key.sort_key,
            **state_item,
        }
        items.append(approval)
    elif state.status == FindingStateStatus.SUBMITTED:
        submission_key = keys.build_key(
            facet=TABLE.facets["finding_submission"],
            values={"group_name": group_name, "id": finding_id},
        )
        submission = {
            key_structure.partition_key: submission_key.partition_key,
            key_structure.sort_key: submission_key.sort_key,
            **state_item,
        }
        items.append(submission)
    await operations.batch_put_item(items=tuple(items), table=TABLE)

    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    metadata_item = {"state": state_item}
    if state.status == FindingStateStatus.APPROVED:
        metadata_item["approval"] = state_item
    elif state.status == FindingStateStatus.SUBMITTED:
        metadata_item["submission"] = state_item
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists()
        & Attr("state.status").ne(FindingStateStatus.DELETED.value)
        & Attr("state.modified_date").eq(current_value.modified_date),
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )


async def update_unreliable_indicators(
    *,
    current_value: FindingUnreliableIndicators,
    group_name: str,
    finding_id: str,
    indicators: FindingUnreliableIndicatorsToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    unreliable_indicators_key = keys.build_key(
        facet=TABLE.facets["finding_unreliable_indicators"],
        values={"group_name": group_name, "id": finding_id},
    )
    unreliable_indicators_item = {
        key: value.value
        if isinstance(value, Enum)
        else format_treatment_summary_item(value)
        if isinstance(value, FindingTreatmentSummary)
        else format_verification_summary_item(value)
        if isinstance(value, FindingVerificationSummary)
        else value
        for key, value in indicators._asdict().items()
        if value is not None
    }
    current_value_item = format_unreliable_indicators_item(current_value)
    conditions = (
        Attr(indicator_name).eq(current_value_item[indicator_name])
        for indicator_name in unreliable_indicators_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=unreliable_indicators_item,
            key=unreliable_indicators_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise IndicatorAlreadyUpdated() from ex

    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    unreliable_indicators_item = {
        f"unreliable_indicators.{key}": value.value
        if isinstance(value, Enum)
        else format_treatment_summary_item(value)
        if isinstance(value, FindingTreatmentSummary)
        else format_verification_summary_item(value)
        if isinstance(value, FindingVerificationSummary)
        else value
        for key, value in indicators._asdict().items()
        if value is not None
    }
    current_value_item = {
        f"unreliable_indicators.{key}": value
        for key, value in current_value_item.items()
    }
    conditions = (
        (
            Attr(indicator_name).not_exists()
            | Attr(indicator_name).eq(current_value_item[indicator_name])
        )
        for indicator_name in unreliable_indicators_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=unreliable_indicators_item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise IndicatorAlreadyUpdated() from ex


async def update_verification(
    *,
    current_value: Optional[FindingVerification],
    group_name: str,
    finding_id: str,
    verification: FindingVerification,
) -> None:
    key_structure = TABLE.primary_key
    verification_item = format_verification_item(verification)
    latest, historic = historics.build_historic(
        attributes=verification_item,
        historic_facet=TABLE.facets["finding_historic_verification"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": verification.modified_date,
            "group_name": group_name,
            "id": finding_id,
        },
        latest_facet=TABLE.facets["finding_verification"],
    )
    await operations.put_item(
        condition_expression=(
            Attr("modified_date").eq(current_value.modified_date)
            if current_value
            else None
        ),
        facet=TABLE.facets["finding_verification"],
        item=latest,
        table=TABLE,
    )
    await operations.put_item(
        facet=TABLE.facets["finding_historic_verification"],
        item=historic,
        table=TABLE,
    )

    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    metadata_item = {"verification": verification_item}
    condition_expression = Attr(key_structure.partition_key).exists()
    if current_value:
        condition_expression &= Attr("verification.modified_date").eq(
            current_value.modified_date
        )
    await operations.update_item(
        condition_expression=condition_expression,
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )
