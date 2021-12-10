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
import simplejson as json  # type: ignore
from typing import (
    Optional,
)


async def update_metadata(
    *,
    finding_id: str,
    metadata: VulnerabilityMetadataToUpdate,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id, "id": vulnerability_id},
    )
    vulnerability_item = json.loads(json.dumps(metadata))
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=vulnerability_item,
        key=vulnerability_key,
        table=TABLE,
    )


async def update_state(
    *,
    current_value: VulnerabilityState,
    finding_id: str,
    state: VulnerabilityState,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state))

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={
                "finding_id": finding_id,
                "id": vulnerability_id,
            },
        )
        vulnerability_item = {"state": state_item}
        await operations.update_item(
            condition_expression=(
                Attr("state.status").ne(VulnerabilityStateStatus.DELETED.value)
                & Attr("state.modified_date").eq(current_value.modified_date)
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    state_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_state"],
        values={
            "id": vulnerability_id,
            "iso8601utc": state.modified_date,
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["vulnerability_historic_state"],
        item=historic_state_item,
        table=TABLE,
    )


async def update_treatment(
    *,
    current_value: VulnerabilityTreatment,
    finding_id: str,
    treatment: VulnerabilityTreatment,
    vulnerability_id: str,
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
            "id": vulnerability_id,
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
    vulnerability_id: str,
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
            "id": vulnerability_id,
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
    vulnerability_id: str,
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
            "id": vulnerability_id,
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
