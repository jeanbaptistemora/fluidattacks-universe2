# Standard
from typing import Optional, Tuple, Union

# Third party
from aiodataloader import DataLoader
from aioextensions import collect
from boto3.dynamodb.conditions import Key

# Local
from custom_exceptions import FindingNotFound
from dynamodb import historics, keys, operations
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from model import TABLE
from .types import (
    Finding,
    FindingEvidence,
    FindingEvidences,
    FindingRecords,
    FindingState,
    FindingVerification,
    Finding20Severity,
    Finding31Severity,
)
from .utils import (
    format_state,
    format_verification,
)


def _build_finding(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> Finding:
    metadata = historics.get_metadata(
        item_id=item_id,
        key_structure=key_structure,
        raw_items=raw_items
    )
    state = format_state(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_prefix='STATE',
            raw_items=raw_items
        )
    )
    try:
        approval: Optional[FindingState] = format_state(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_prefix='APPROVAL',
                raw_items=raw_items
            )
        )
    except StopIteration:
        approval = None
    try:
        creation: Optional[FindingState] = format_state(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_prefix='CREATION',
                raw_items=raw_items
            )
        )
    except StopIteration:
        creation = None
    try:
        submission: Optional[FindingState] = format_state(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_prefix='SUBMISSION',
                raw_items=raw_items
            )
        )
    except StopIteration:
        submission = None
    try:
        verification: Optional[FindingVerification] = format_verification(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_prefix='VERIFICATION',
                raw_items=raw_items
            )
        )
    except StopIteration:
        verification = None

    if metadata['cvss_version'] == '3.1':
        severity: Union[Finding20Severity, Finding31Severity] = (
            Finding31Severity(**{
                field: metadata['severity'][field]
                for field in Finding31Severity._fields
            })
        )
    else:
        severity = Finding20Severity(**{
            field: metadata['severity'][field]
            for field in Finding20Severity._fields
        })
    evidences = FindingEvidences(
        animation=FindingEvidence(**metadata['evidences']['animation']),
        evidence1=FindingEvidence(**metadata['evidences']['evidence1']),
        evidence2=FindingEvidence(**metadata['evidences']['evidence2']),
        evidence3=FindingEvidence(**metadata['evidences']['evidence3']),
        evidence4=FindingEvidence(**metadata['evidences']['evidence4']),
        evidence5=FindingEvidence(**metadata['evidences']['evidence5']),
        exploitation=FindingEvidence(**metadata['evidences']['exploitation']),
    )

    return Finding(
        actor=metadata['actor'],
        affected_systems=metadata['affected_systems'],
        analyst_email=metadata['analyst_email'],
        approval=approval,
        attack_vector_desc=metadata['attack_vector_desc'],
        bts_url=metadata['bts_url'],
        compromised_attributes=metadata['compromised_attributes'],
        compromised_records=metadata['compromised_records'],
        creation=creation,
        cvss_version=metadata['cvss_version'],
        cwe=metadata['cwe'],
        description=metadata['description'],
        evidences=evidences,
        group_name=metadata['group_name'],
        id=metadata['id'],
        scenario=metadata['scenario'],
        severity=severity,
        sorts=metadata['sorts'],
        submission=submission,
        records=FindingRecords(**metadata['records']),
        recommendation=metadata['recommendation'],
        requirements=metadata['requirements'],
        risk=metadata['risk'],
        title=metadata['title'],
        threat=metadata['threat'],
        type=metadata['type'],
        state=state,
        verification=verification
    )


async def _get_finding(
    *,
    group_name: str,
    finding_id: str
) -> Finding:
    primary_key = keys.build_key(
        facet=TABLE.facets['finding_metadata'],
        values={'group_name': group_name, 'id': finding_id},
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key) &
            Key(key_structure.sort_key).begins_with(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets['finding_approval'],
            TABLE.facets['finding_creation'],
            TABLE.facets['finding_metadata'],
            TABLE.facets['finding_state'],
            TABLE.facets['finding_submission'],
            TABLE.facets['finding_verification'],
        ),
        index=index,
        table=TABLE
    )

    if not results:
        raise FindingNotFound()

    return _build_finding(
        item_id=primary_key.partition_key,
        key_structure=key_structure,
        raw_items=results
    )


class FindingNewLoader(DataLoader):
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        finding: Tuple[Tuple[str, str], ...]
    ) -> Tuple[Finding, ...]:
        return tuple(await collect(
            _get_finding(group_name=group_name, finding_id=finding_id)
            for group_name, finding_id in finding
        ))
