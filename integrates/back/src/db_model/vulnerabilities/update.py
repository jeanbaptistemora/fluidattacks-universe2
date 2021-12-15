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
    historic_entry_type_to_str,
    VulnerabilityHistoric,
    VulnerabilityHistoricEntry,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from custom_exceptions import (
    VulnNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore
from typing import (
    Optional,
    Tuple,
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
    vulnerability_item = {
        key: value
        for key, value in json.loads(json.dumps(metadata)).items()
        if value is not None
    }
    if vulnerability_item:
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
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
            values={"finding_id": finding_id, "id": vulnerability_id},
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
        values={"id": vulnerability_id, "iso8601utc": state.modified_date},
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


async def update_historic_state(
    *,
    finding_id: str,
    historic_state: Tuple[VulnerabilityState, ...],
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {
            "state": json.loads(json.dumps(historic_state[-1]))
        }
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_state"],
        values={"id": vulnerability_id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_state"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_state"],
            values={
                "id": vulnerability_id,
                "iso8601utc": item["modified_date"],
            },
        )
        for item in current_items
    }

    new_keys = {
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_state"],
            values={
                "id": vulnerability_id,
                "iso8601utc": state.modified_date,
            },
        )
        for state in historic_state
    }
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(state)),
        }
        for key, state in zip(new_keys, historic_state)
    )
    await operations.batch_write_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )


async def update_treatment(
    *,
    current_value: Optional[VulnerabilityTreatment],
    finding_id: str,
    treatment: VulnerabilityTreatment,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    treatment_item = json.loads(json.dumps(treatment))

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {"treatment": treatment_item}
        base_condition = Attr("state.status").ne(
            VulnerabilityStateStatus.DELETED.value
        )
        await operations.update_item(
            condition_expression=(
                base_condition
                & Attr("treatment.modified_date").eq(
                    current_value.modified_date
                )
                if current_value
                else base_condition
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    treatment_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_treatment"],
        values={
            "id": vulnerability_id,
            "iso8601utc": treatment.modified_date,
        },
    )
    historic_treatment_item = {
        key_structure.partition_key: treatment_key.partition_key,
        key_structure.sort_key: treatment_key.sort_key,
        **treatment_item,
    }
    await operations.put_item(
        facet=TABLE.facets["vulnerability_historic_treatment"],
        item=historic_treatment_item,
        table=TABLE,
    )


async def update_historic_treatment(
    *,
    finding_id: str,
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {
            "treatment": json.loads(json.dumps(historic_treatment[-1]))
        }
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_treatment"],
        values={"id": vulnerability_id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_treatment"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_treatment"],
            values={
                "id": vulnerability_id,
                "iso8601utc": item["modified_date"],
            },
        )
        for item in current_items
    }

    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_treatment"],
            values={
                "id": vulnerability_id,
                "iso8601utc": treatment.modified_date,
            },
        )
        for treatment in historic_treatment
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(treatment)),
        }
        for key, treatment in zip(new_keys, historic_treatment)
    )
    await operations.batch_write_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )


async def update_verification(
    *,
    current_value: Optional[VulnerabilityVerification],
    finding_id: str,
    vulnerability_id: str,
    verification: VulnerabilityVerification,
) -> None:
    key_structure = TABLE.primary_key
    verification_item = json.loads(json.dumps(verification))

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {"verification": verification_item}
        base_condition = Attr("state.status").ne(
            VulnerabilityStateStatus.DELETED.value
        )
        await operations.update_item(
            condition_expression=(
                base_condition
                & Attr("verification.modified_date").eq(
                    current_value.modified_date
                )
                if current_value
                else base_condition
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    verification_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_verification"],
        values={
            "id": vulnerability_id,
            "iso8601utc": verification.modified_date,
        },
    )
    historic_verification_item = {
        key_structure.partition_key: verification_key.partition_key,
        key_structure.sort_key: verification_key.sort_key,
        **verification_item,
    }
    await operations.put_item(
        facet=TABLE.facets["vulnerability_historic_verification"],
        item=historic_verification_item,
        table=TABLE,
    )


async def update_historic_verification(
    *,
    finding_id: str,
    historic_verification: Tuple[VulnerabilityVerification, ...],
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {
            "verification": json.loads(json.dumps(historic_verification[-1]))
        }
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_verification"],
        values={"id": vulnerability_id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_verification"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_verification"],
            values={
                "id": vulnerability_id,
                "iso8601utc": item["modified_date"],
            },
        )
        for item in current_items
    }

    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_verification"],
            values={
                "id": vulnerability_id,
                "iso8601utc": verification.modified_date,
            },
        )
        for verification in historic_verification
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(verification)),
        }
        for key, verification in zip(new_keys, historic_verification)
    )
    await operations.batch_write_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )


async def update_zero_risk(
    *,
    current_value: Optional[VulnerabilityZeroRisk],
    finding_id: str,
    vulnerability_id: str,
    zero_risk: VulnerabilityZeroRisk,
) -> None:
    key_structure = TABLE.primary_key
    zero_risk_item = json.loads(json.dumps(zero_risk))

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {"zero_risk": zero_risk_item}
        base_condition = Attr("state.status").ne(
            VulnerabilityStateStatus.DELETED.value
        )
        await operations.update_item(
            condition_expression=(
                base_condition
                & Attr("zero_risk.modified_date").eq(
                    current_value.modified_date
                )
                if current_value
                else base_condition
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    zero_risk_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_zero_risk"],
        values={
            "id": vulnerability_id,
            "iso8601utc": zero_risk.modified_date,
        },
    )
    historic_zero_risk_item = {
        key_structure.partition_key: zero_risk_key.partition_key,
        key_structure.sort_key: zero_risk_key.sort_key,
        **zero_risk_item,
    }
    await operations.put_item(
        facet=TABLE.facets["vulnerability_historic_zero_risk"],
        item=historic_zero_risk_item,
        table=TABLE,
    )


async def update_historic_zero_risk(
    *,
    finding_id: str,
    historic_zero_risk: Tuple[VulnerabilityZeroRisk, ...],
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {
            "zero_risk": json.loads(json.dumps(historic_zero_risk[-1]))
        }
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_zero_risk"],
        values={"id": vulnerability_id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_zero_risk"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_zero_risk"],
            values={
                "id": vulnerability_id,
                "iso8601utc": item["modified_date"],
            },
        )
        for item in current_items
    }

    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["vulnerability_historic_zero_risk"],
            values={
                "id": vulnerability_id,
                "iso8601utc": zero_risk.modified_date,
            },
        )
        for zero_risk in historic_zero_risk
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(zero_risk)),
        }
        for key, zero_risk in zip(new_keys, historic_zero_risk)
    )
    await operations.batch_write_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )


async def update_historic_entry(
    *,
    current_entry: Optional[VulnerabilityHistoricEntry],
    finding_id: str,
    entry: VulnerabilityHistoricEntry,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    entry_type = historic_entry_type_to_str(entry)
    entry_item = json.loads(json.dumps(entry))

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {entry_type: entry_item}
        base_condition = Attr("state.status").ne(
            VulnerabilityStateStatus.DELETED.value
        )
        await operations.update_item(
            condition_expression=(
                base_condition
                & Attr(f"{entry_type}.modified_date").eq(
                    current_entry.modified_date
                )
                if current_entry
                else base_condition
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_entry_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={
            "id": vulnerability_id,
            "iso8601utc": entry.modified_date,
        },
    )
    historic_item = {
        key_structure.partition_key: historic_entry_key.partition_key,
        key_structure.sort_key: historic_entry_key.sort_key,
        **entry_item,
    }
    await operations.put_item(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        item=historic_item,
        table=TABLE,
    )


async def update_historic(
    *,
    finding_id: str,
    historic: VulnerabilityHistoric,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    latest_entry = historic[-1]
    entry_type = historic_entry_type_to_str(latest_entry)

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {entry_type: json.loads(json.dumps(latest_entry))}
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={"id": vulnerability_id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets[f"vulnerability_historic_{entry_type}"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": vulnerability_id,
                "iso8601utc": item["modified_date"],
            },
        )
        for item in current_items
    }

    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": vulnerability_id,
                "iso8601utc": entry.modified_date,
            },
        )
        for entry in historic
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(entry)),
        }
        for key, entry in zip(new_keys, historic)
    )
    await operations.batch_write_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )
