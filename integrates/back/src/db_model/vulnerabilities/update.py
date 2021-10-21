from .enums import (
    VulnerabilityStateStatus,
)
from .types import (
    VulnerabilityMetadataToUpdate,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from .utils import (
    format_state_item,
    format_treatment_item,
    format_verification_item,
    format_zero_risk_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    VulnNotFound,
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
    Optional,
)


async def update_metadata(
    *,
    finding_id: str,
    metadata: VulnerabilityMetadataToUpdate,
    uuid: str,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id, "uuid": uuid},
    )
    metadata_item = {
        key: value.value if isinstance(value, Enum) else value._asdict()
        for key, value in metadata._asdict().items()
        if value is not None
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )


async def update_state(
    *,
    current_value: VulnerabilityState,
    finding_id: str,
    state: VulnerabilityState,
    uuid: str,
) -> None:
    items = []
    key_structure = TABLE.primary_key
    state_item = format_state_item(state)
    latest, historic = historics.build_historic(
        attributes=state_item,
        historic_facet=TABLE.facets["vulnerability_historic_state"],
        key_structure=key_structure,
        key_values={
            "finding_id": finding_id,
            "iso8601utc": state.modified_date,
            "uuid": uuid,
        },
        latest_facet=TABLE.facets["vulnerability_state"],
    )
    try:
        await operations.put_item(
            condition_expression=(
                Attr("status").ne(VulnerabilityStateStatus.DELETED.value)
                & Attr("modified_date").eq(current_value.modified_date)
            ),
            facet=TABLE.facets["vulnerability_state"],
            item=latest,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)


async def update_treatment(
    *,
    current_value: VulnerabilityTreatment,
    finding_id: str,
    treatment: VulnerabilityTreatment,
    uuid: str,
) -> None:
    items = []
    key_structure = TABLE.primary_key
    treatment_item = format_treatment_item(treatment)
    latest, historic = historics.build_historic(
        attributes=treatment_item,
        historic_facet=TABLE.facets["vulnerability_historic_treatment"],
        key_structure=key_structure,
        key_values={
            "finding_id": finding_id,
            "iso8601utc": treatment.modified_date,
            "uuid": uuid,
        },
        latest_facet=TABLE.facets["vulnerability_treatment"],
    )
    try:
        await operations.put_item(
            condition_expression=(
                Attr("modified_date").eq(current_value.modified_date)
            ),
            facet=TABLE.facets["vulnerability_treatment"],
            item=latest,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)


async def update_verification(
    *,
    current_value: Optional[VulnerabilityVerification],
    finding_id: str,
    uuid: str,
    verification: VulnerabilityVerification,
) -> None:
    items = []
    key_structure = TABLE.primary_key
    verification_item = format_verification_item(verification)
    latest, historic = historics.build_historic(
        attributes=verification_item,
        historic_facet=TABLE.facets["vulnerability_historic_verification"],
        key_structure=key_structure,
        key_values={
            "finding_id": finding_id,
            "iso8601utc": verification.modified_date,
            "uuid": uuid,
        },
        latest_facet=TABLE.facets["vulnerability_verification"],
    )
    try:
        await operations.put_item(
            condition_expression=(
                Attr("modified_date").eq(current_value.modified_date)
                if current_value
                else None
            ),
            facet=TABLE.facets["vulnerability_verification"],
            item=latest,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)


async def update_zero_risk(
    *,
    current_value: Optional[VulnerabilityZeroRisk],
    finding_id: str,
    uuid: str,
    zero_risk: VulnerabilityZeroRisk,
) -> None:
    items = []
    key_structure = TABLE.primary_key
    zero_risk_item = format_zero_risk_item(zero_risk)
    latest, historic = historics.build_historic(
        attributes=zero_risk_item,
        historic_facet=TABLE.facets["vulnerability_historic_zero_risk"],
        key_structure=key_structure,
        key_values={
            "finding_id": finding_id,
            "iso8601utc": zero_risk.modified_date,
            "uuid": uuid,
        },
        latest_facet=TABLE.facets["vulnerability_zero_risk"],
    )
    try:
        await operations.put_item(
            condition_expression=(
                Attr("modified_date").eq(current_value.modified_date)
                if current_value
                else None
            ),
            facet=TABLE.facets["vulnerability_zero_risk"],
            item=latest,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)
