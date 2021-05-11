
from dynamodb import (
    historics,
    keys,
    operations,
)
from model import TABLE

from .types import Finding
from .utils import (
    format_state_item,
    format_verification_item,
)


async def create(*, finding: Finding) -> None:
    items = []
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets['finding_metadata'],
        values={'group_name': finding.group_name, 'id': finding.id},
    )
    metadata_evidences = {
        field: evidence._asdict()
        for field, evidence
        in finding.evidences._asdict().items()
    }
    finding_metadata = {
        'actor': finding.actor,
        'affected_systems': finding.affected_systems,
        'analyst_email': finding.analyst_email,
        'attack_vector_desc': finding.attack_vector_desc,
        'bts_url': finding.bts_url,
        'compromised_attributes': finding.compromised_attributes,
        'compromised_records': finding.compromised_records,
        'cvss_version': finding.cvss_version,
        'cwe': finding.cwe,
        'description': finding.description,
        'evidences': metadata_evidences,
        'group_name': finding.group_name,
        'id': finding.id,
        'scenario': finding.scenario,
        'severity': finding.severity._asdict(),
        'sorts': finding.sorts.value,
        'records': finding.records._asdict(),
        'risk': finding.risk,
        'recommendation': finding.recommendation,
        'requirements': finding.requirements,
        'title': finding.title,
        'threat': finding.threat,
        'type': finding.type,
    }
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **finding_metadata
    }
    items.append(initial_metadata)
    state_item = format_state_item(finding.state)
    historic_state = historics.build_historic(
        attributes=state_item,
        historic_facet=TABLE.facets['finding_historic_state'],
        key_structure=key_structure,
        key_values={
            'iso8601utc': finding.state.modified_date,
            'group_name': finding.group_name,
            'id': finding.id
        },
        latest_facet=TABLE.facets['finding_state'],
    )
    items.extend(historic_state)
    creation_key = keys.build_key(
        facet=TABLE.facets['finding_creation'],
        values={'group_name': finding.group_name, 'id': finding.id},
    )
    creation = {
        key_structure.partition_key: creation_key.partition_key,
        key_structure.sort_key: creation_key.sort_key,
        **state_item
    }
    items.append(creation)

    if finding.verification:
        historic_verification = historics.build_historic(
            attributes=format_verification_item(finding.verification),
            historic_facet=TABLE.facets['finding_historic_verification'],
            key_structure=key_structure,
            key_values={
                'iso8601utc': finding.state.modified_date,
                'group_name': finding.group_name,
                'id': finding.id
            },
            latest_facet=TABLE.facets['finding_verification'],
        )
        items.extend(historic_verification)

    await operations.batch_write_item(items=tuple(items), table=TABLE)
