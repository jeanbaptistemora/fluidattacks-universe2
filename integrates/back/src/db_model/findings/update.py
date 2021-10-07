from .enums import (
    FindingCvssVersion,
    FindingEvidenceName,
    FindingStateStatus,
)
from .types import (
    Finding20Severity,
    Finding31Severity,
    FindingEvidences,
    FindingEvidenceToUpdate,
    FindingMetadataToUpdate,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from .utils import (
    format_evidences_item,
    format_state_item,
    format_treatment_summary_item,
    format_verification_item,
    get_latest_verification,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from custom_exceptions import (
    FindingNotFound,
)
from db_model import (
    TABLE,
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
    Tuple,
)


async def update_evidence(
    *,
    group_name: str,
    finding_id: str,
    evidence_name: FindingEvidenceName,
    evidence: FindingEvidenceToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    metadata_item = {
        f"evidences.{evidence_name.value}.{key}": value
        for key, value in evidence._asdict().items()
        if value is not None
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )


async def update_historic_verification(  # pylint: disable=too-many-locals
    *,
    group_name: str,
    finding_id: str,
    historic_verification: Tuple[FindingVerification, ...],
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_verification"],
        values={"id": finding_id},
    )
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_verification"],),
        table=TABLE,
    )
    current_verification_keys = {
        keys.build_key(
            facet=TABLE.facets["finding_historic_verification"],
            values={
                "iso8601utc": item["modified_date"],
                "id": finding_id,
            },
        )
        for item in results
    }
    verification_items = []
    verification_keys = set()
    for verification in historic_verification:
        verification_item = format_verification_item(verification)
        verification_key = keys.build_key(
            facet=TABLE.facets["finding_historic_verification"],
            values={
                "iso8601utc": verification.modified_date,
                "id": finding_id,
            },
        )
        verification_keys.add(verification_key)
        verification_item = {
            key_structure.partition_key: verification_key.partition_key,
            key_structure.sort_key: verification_key.sort_key,
            **verification_item,
        }
        verification_items.append(verification_item)
    latest_verification = get_latest_verification(historic_verification)
    if latest_verification:
        latest_key = keys.build_key(
            facet=TABLE.facets["finding_verification"],
            values={
                "group_name": group_name,
                "id": finding_id,
            },
        )
        latest_optional_item = format_verification_item(latest_verification)
        latest_item = {
            key_structure.partition_key: latest_key.partition_key,
            key_structure.sort_key: latest_key.sort_key,
            **latest_optional_item,
        }
        verification_items.append(latest_item)

    operation_coroutines = [
        operations.batch_write_item(
            items=tuple(verification_items), table=TABLE
        )
    ]
    verifications_to_remove = [
        current_verification_key
        for current_verification_key in current_verification_keys
        if current_verification_key not in verification_keys
    ]
    operation_coroutines.append(
        operations.batch_delete_item(
            keys=verifications_to_remove,
            table=TABLE,
        )
    )
    await collect(operation_coroutines)


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


async def update_state(
    *,
    group_name: str,
    finding_id: str,
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
    condition_expression = Attr(key_structure.partition_key).exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
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
    await operations.batch_write_item(items=tuple(items), table=TABLE)


async def update_unreliable_indicators(
    *,
    group_name: str,
    finding_id: str,
    indicators: FindingUnreliableIndicatorsToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    unreliable_indicators_key = keys.build_key(
        facet=TABLE.facets["finding_unreliable_indicators"],
        values={"group_name": group_name, "id": finding_id},
    )
    unreliable_indicators = {
        key: value.value
        if isinstance(value, Enum)
        else format_treatment_summary_item(value)
        if isinstance(value, FindingTreatmentSummary)
        else value
        for key, value in indicators._asdict().items()
        if value is not None
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=unreliable_indicators,
        key=unreliable_indicators_key,
        table=TABLE,
    )


async def update_verification(
    *,
    group_name: str,
    finding_id: str,
    verification: FindingVerification,
) -> None:
    items = []
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
        facet=TABLE.facets["finding_verification"],
        item=latest,
        table=TABLE,
    )
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)
