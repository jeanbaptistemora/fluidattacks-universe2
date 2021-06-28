from .types import (
    Finding,
)
from .utils import (
    format_optional_verification_item,
    format_state_item,
    format_unreliable_indicators_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    AlreadyCreated,
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


async def create(  # pylint: disable=too-many-locals
    *, finding: Finding
) -> None:
    key_structure = TABLE.primary_key
    id_key = keys.build_key(
        facet=TABLE.facets["finding_id"],
        values={"id": finding.id},
    )
    id_item = {
        key_structure.partition_key: id_key.partition_key,
        key_structure.sort_key: id_key.sort_key,
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["finding_id"],
            item=id_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException:
        raise AlreadyCreated()
    items = []
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": finding.group_name, "id": finding.id},
    )
    metadata_evidences = {
        field: evidence._asdict()
        for field, evidence in finding.evidences._asdict().items()
        if evidence is not None
    }
    finding_metadata = {
        "actor": finding.actor,
        "affected_systems": finding.affected_systems,
        "analyst_email": finding.analyst_email,
        "attack_vector_desc": finding.attack_vector_desc,
        "bts_url": finding.bts_url,
        "compromised_attributes": finding.compromised_attributes,
        "compromised_records": finding.compromised_records,
        "cvss_version": finding.cvss_version,
        "cwe": finding.cwe,
        "description": finding.description,
        "evidences": metadata_evidences,
        "group_name": finding.group_name,
        "id": finding.id,
        "scenario": finding.scenario,
        "severity": finding.severity._asdict(),
        "sorts": finding.sorts.value,
        "risk": finding.risk,
        "recommendation": finding.recommendation,
        "requirements": finding.requirements,
        "title": finding.title,
        "threat": finding.threat,
        "type": finding.type,
    }
    if finding.records is not None:
        finding_metadata["records"] = finding.records._asdict()
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **finding_metadata,
    }
    items.append(initial_metadata)
    state_item = format_state_item(finding.state)
    historic_state = historics.build_historic(
        attributes=state_item,
        historic_facet=TABLE.facets["finding_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": finding.state.modified_date,
            "group_name": finding.group_name,
            "id": finding.id,
        },
        latest_facet=TABLE.facets["finding_state"],
    )
    items.extend(historic_state)
    creation_key = keys.build_key(
        facet=TABLE.facets["finding_creation"],
        values={"group_name": finding.group_name, "id": finding.id},
    )
    creation = {
        key_structure.partition_key: creation_key.partition_key,
        key_structure.sort_key: creation_key.sort_key,
        **state_item,
    }
    items.append(creation)
    unreliable_indicators_key = keys.build_key(
        facet=TABLE.facets["finding_unreliable_indicators"],
        values={"group_name": finding.group_name, "id": finding.id},
    )
    unreliable_indicators_item = format_unreliable_indicators_item(
        finding.unreliable_indicators
    )
    unreliable_indicators = {
        key_structure.partition_key: unreliable_indicators_key.partition_key,
        key_structure.sort_key: unreliable_indicators_key.sort_key,
        **unreliable_indicators_item,
    }
    items.append(unreliable_indicators)
    latest_verification, historic_verification = historics.build_historic(
        attributes=format_optional_verification_item(finding.verification),
        historic_facet=TABLE.facets["finding_historic_verification"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": finding.state.modified_date,
            "group_name": finding.group_name,
            "id": finding.id,
        },
        latest_facet=TABLE.facets["finding_verification"],
    )
    if finding.verification:
        items.append(latest_verification)
        items.append(historic_verification)
    else:
        items.append(latest_verification)

    await operations.batch_write_item(items=tuple(items), table=TABLE)
