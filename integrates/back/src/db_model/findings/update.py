from .enums import (
    FindingCvssVersion,
    FindingEvidenceName,
    FindingStateStatus,
)
from .utils import (
    format_evidence_item,
    format_evidences_item,
    format_state_item,
    format_unreliable_indicators_item,
    format_unreliable_indicators_to_update_item,
    format_verification_item,
    get_finding_current_state_converted,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    EmptyHistoric,
    FindingNotFound,
    IndicatorAlreadyUpdated,
)
from db_model import (
    TABLE,
    utils as db_model_utils,
)
from db_model.findings.constants import (
    ME_DRAFTS_INDEX_METADATA,
)
from db_model.findings.types import (
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingEvidenceToUpdate,
    FindingMetadataToUpdate,
    FindingState,
    FindingUnreliableIndicators,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    Item,
)
from enum import (
    Enum,
)
import simplejson as json
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
    evidence_item: Item = json.loads(json.dumps(evidence, default=serialize))
    await operations.update_item(
        condition_expression=Attr(attribute).eq(
            format_evidence_item(current_value)
        ),
        item={
            f"{attribute}.{key}": value
            for key, value in evidence_item.items()
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
    item = {
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
    }
    await operations.update_item(
        condition_expression=(base_condition),
        item=item,
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
    if "hacker_email" in metadata_item:
        metadata_item["analyst_email"] = metadata_item.pop("hacker_email")
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )


async def update_state(
    *,
    current_value: FindingState,
    finding_id: str,
    group_name: str,
    state: FindingState,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    state = state._replace(
        modified_date=db_model_utils.get_datetime_with_offset(
            current_value.modified_date,
            state.modified_date,
        )
    )
    state_item = format_state_item(state)
    metadata_item = {"state": state_item}
    if state.status == FindingStateStatus.APPROVED:
        metadata_item["approval"] = state_item
    elif state.status == FindingStateStatus.SUBMITTED:
        metadata_item["submission"] = state_item
    try:
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists()
            & Attr("state.modified_date").eq(
                get_as_utc_iso_format(current_value.modified_date)
            ),
            item=metadata_item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise FindingNotFound() from ex

    state_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={
            "id": finding_id,
            "iso8601utc": get_as_utc_iso_format(state.modified_date),
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["finding_historic_state"],
        item=historic_state_item,
        table=TABLE,
    )


async def update_historic_state(
    *,
    group_name: str,
    finding_id: str,
    historic_state: tuple[FindingState, ...],
) -> None:
    if not historic_state:
        raise EmptyHistoric()

    historic_state = db_model_utils.adjust_historic_dates(historic_state)
    item = {"state": format_state_item(historic_state[-1])}
    creation = next(
        state
        for state in historic_state
        if state.status == FindingStateStatus.CREATED
    )
    item["creation"] = format_state_item(creation)
    submission = next(
        (
            state
            for state in reversed(historic_state)
            if state.status == FindingStateStatus.SUBMITTED
        ),
        None,
    )
    if submission:
        item["submission"] = format_state_item(submission)
    approval = next(
        (
            state
            for state in reversed(historic_state)
            if state.status == FindingStateStatus.APPROVED
        ),
        None,
    )
    if approval:
        item["approval"] = format_state_item(approval)

    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    try:
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=item,
            key=primary_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise FindingNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={"id": finding_id},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_state"],),
        table=TABLE,
    )
    current_keys = {
        keys.build_key(
            facet=TABLE.facets["finding_historic_state"],
            values={
                "iso8601utc": item["modified_date"],
                "id": finding_id,
            },
        )
        for item in response.items
    }
    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["finding_historic_state"],
            values={
                "id": finding_id,
                "iso8601utc": get_as_utc_iso_format(entry.modified_date),
            },
        )
        for entry in historic_state
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **format_state_item(entry),
        }
        for key, entry in zip(new_keys, historic_state)
    )
    await operations.batch_put_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
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
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    unreliable_indicators_item = {
        f"unreliable_indicators.{key}": value
        for key, value in format_unreliable_indicators_to_update_item(
            indicators
        ).items()
    }
    current_value_item = {
        f"unreliable_indicators.{key}": value
        for key, value in format_unreliable_indicators_item(
            current_value
        ).items()
    }
    conditions = (
        (
            Attr(indicator_name).not_exists()
            | Attr(indicator_name).eq(current_value_item[indicator_name])
        )
        for indicator_name in unreliable_indicators_item
    )
    alt_conditions = (
        (
            Attr(indicator_name).not_exists()
            | Attr(indicator_name).eq(
                get_finding_current_state_converted(
                    current_value_item[indicator_name]
                )
                if indicator_name == "unreliable_indicators.unreliable_status"
                else current_value_item[indicator_name]
            )
        )
        for indicator_name in unreliable_indicators_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    alt_condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    for condition in alt_conditions:
        alt_condition_expression &= condition
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=unreliable_indicators_item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        with suppress(ConditionalCheckFailedException):
            await operations.update_item(
                condition_expression=alt_condition_expression,
                item=unreliable_indicators_item,
                key=metadata_key,
                table=TABLE,
            )
            return

        raise IndicatorAlreadyUpdated() from ex


async def update_verification(
    *,
    current_value: Optional[FindingVerification],
    group_name: str,
    finding_id: str,
    verification: FindingVerification,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    verification_item = format_verification_item(verification)
    metadata_item = {"verification": verification_item}
    condition_expression = Attr(key_structure.partition_key).exists()
    if current_value:
        condition_expression &= Attr("verification.modified_date").eq(
            get_as_utc_iso_format(current_value.modified_date)
        )
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=metadata_item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise FindingNotFound() from ex

    verification_key = keys.build_key(
        facet=TABLE.facets["finding_historic_verification"],
        values={
            "id": finding_id,
            "iso8601utc": get_as_utc_iso_format(verification.modified_date),
        },
    )
    historic_verification_item = {
        key_structure.partition_key: verification_key.partition_key,
        key_structure.sort_key: verification_key.sort_key,
        **verification_item,
    }
    await operations.put_item(
        facet=TABLE.facets["finding_historic_verification"],
        item=historic_verification_item,
        table=TABLE,
    )
