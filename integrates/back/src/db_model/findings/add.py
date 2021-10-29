from .enums import (
    FindingCvssVersion,
    FindingEvidenceName,
)
from .types import (
    Finding,
    Finding31Severity,
    FindingEvidence,
)
from .utils import (
    format_evidence_item,
    format_evidences_item,
    format_state_item,
    format_unreliable_indicators_item,
    format_verification_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    AlreadyCreated,
    InvalidStateStatus,
)
from db_model import (
    TABLE,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)


async def add(*, finding: Finding) -> None:  # pylint: disable=too-many-locals
    if finding.state.status != FindingStateStatus.CREATED:
        raise InvalidStateStatus()
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
    except ConditionalCheckFailedException as ex:
        raise AlreadyCreated() from ex
    items = []
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": finding.group_name, "id": finding.id},
    )
    metadata_evidences_item = format_evidences_item(finding.evidences)
    cvss_version = (
        FindingCvssVersion.V31
        if isinstance(finding.severity, Finding31Severity)
        else FindingCvssVersion.V20
    )
    finding_metadata = {
        "affected_systems": finding.affected_systems,
        "analyst_email": finding.hacker_email,
        "attack_vector_description": finding.attack_vector_description,
        "cvss_version": cvss_version.value,
        "description": finding.description,
        "evidences": metadata_evidences_item,
        "group_name": finding.group_name,
        "id": finding.id,
        "severity": finding.severity._asdict(),
        "sorts": finding.sorts.value,
        "recommendation": finding.recommendation,
        "requirements": finding.requirements,
        "title": finding.title,
        "threat": finding.threat,
    }
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
    if finding.verification is not None:
        verification, historic_verification = historics.build_historic(
            attributes=format_verification_item(finding.verification),
            historic_facet=TABLE.facets["finding_historic_verification"],
            key_structure=key_structure,
            key_values={
                "iso8601utc": finding.verification.modified_date,
                "group_name": finding.group_name,
                "id": finding.id,
            },
            latest_facet=TABLE.facets["finding_verification"],
        )
        items.append(verification)
        items.append(historic_verification)
    await operations.batch_write_item(items=tuple(items), table=TABLE)


async def add_evidence(
    *,
    evidence_name: FindingEvidenceName,
    evidence: FindingEvidence,
    finding_id: str,
    group_name: str,
) -> None:
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    attribute = f"evidences.{evidence_name.value}"
    await operations.update_item(
        condition_expression=Attr(attribute).not_exists(),
        item={attribute: format_evidence_item(evidence)},
        key=metadata_key,
        table=TABLE,
    )
