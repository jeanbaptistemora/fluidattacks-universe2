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
from db_model.findings.constants import (
    ME_DRAFTS_INDEX_METADATA,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.utils import (
    get_as_utc_iso_format,
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
from typing import (
    Any,
)


async def add(*, finding: Finding) -> None:  # pylint: disable=too-many-locals
    if finding.state.status != FindingStateStatus.CREATED:
        raise InvalidStateStatus()
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    id_key = keys.build_key(
        facet=TABLE.facets["finding_id"],
        values={"id": finding.id},
    )
    gsi_2_key = keys.build_key(
        facet=ME_DRAFTS_INDEX_METADATA,
        values={
            "email": finding.hacker_email,
            "id": finding.id,
        },
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

    items: list[Item] = []
    state_item = format_state_item(finding.state)
    state_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={
            "id": finding.id,
            "iso8601utc": get_as_utc_iso_format(finding.state.modified_date),
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **state_item,
    }
    items.append(historic_state_item)

    if finding.verification is not None:
        verification_item = format_verification_item(finding.verification)
        verification_key = keys.build_key(
            facet=TABLE.facets["finding_historic_verification"],
            values={
                "id": finding.id,
                "iso8601utc": get_as_utc_iso_format(
                    finding.verification.modified_date
                ),
            },
        )
        historic_verification_item = {
            key_structure.partition_key: verification_key.partition_key,
            key_structure.sort_key: verification_key.sort_key,
            **verification_item,
        }
        items.append(historic_verification_item)

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
        "analyst_email": finding.hacker_email,
        "attack_vector_description": finding.attack_vector_description,
        "creation": state_item,
        "cvss_version": cvss_version.value,
        "description": finding.description,
        "evidences": metadata_evidences_item,
        "group_name": finding.group_name,
        "id": finding.id,
        "min_time_to_remediate": finding.min_time_to_remediate,
        "severity": finding.severity._asdict(),
        "severity_score": (
            finding.severity_score._asdict()
            if finding.severity_score
            else None
        ),
        "sorts": finding.sorts.value,
        "state": state_item,
        "recommendation": finding.recommendation,
        "requirements": finding.requirements,
        "title": finding.title,
        "threat": finding.threat,
        "unfulfilled_requirements": finding.unfulfilled_requirements,
        "unreliable_indicators": format_unreliable_indicators_item(
            finding.unreliable_indicators
        ),
        "verification": format_verification_item(finding.verification)
        if finding.verification
        else None,
    }
    initial_metadata: dict[str, Any] = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        **finding_metadata,
    }
    items.append(initial_metadata)

    await operations.batch_put_item(items=tuple(items), table=TABLE)


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
