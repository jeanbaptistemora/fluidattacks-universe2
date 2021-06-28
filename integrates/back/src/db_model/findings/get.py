from .enums import (
    FindingSorts,
    FindingStateStatus,
)
from .types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingRecords,
    FindingState,
    FindingVerification,
)
from .utils import (
    format_optional_verification,
    format_state,
    format_unreliable_indicators,
    format_verification,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
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
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from typing import (
    Optional,
    Tuple,
    Union,
)


def _build_finding(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> Finding:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = format_state(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="STATE",
            raw_items=raw_items,
        )
    )
    unreliable_indicators = format_unreliable_indicators(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="UNRELIABLEINDICATORS",
            raw_items=raw_items,
        )
    )

    try:
        approval: Optional[FindingState] = format_state(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="APPROVAL",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        approval = None
    try:
        creation: Optional[FindingState] = format_state(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="CREATION",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        creation = None
    try:
        submission: Optional[FindingState] = format_state(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="SUBMISSION",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        submission = None
    verification: Optional[FindingVerification] = format_optional_verification(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="VERIFICATION",
            raw_items=raw_items,
        )
    )

    if metadata["cvss_version"] == "3.1":
        severity: Union[
            Finding20Severity, Finding31Severity
        ] = Finding31Severity(
            **{
                field: metadata["severity"][field]
                for field in Finding31Severity._fields
            }
        )
    else:
        severity = Finding20Severity(
            **{
                field: metadata["severity"][field]
                for field in Finding20Severity._fields
            }
        )
    evidences = FindingEvidences(
        **{
            name: FindingEvidence(**evidence)
            for name, evidence in metadata["evidences"].items()
        }
    )

    return Finding(
        actor=metadata["actor"],
        affected_systems=metadata["affected_systems"],
        analyst_email=metadata["analyst_email"],
        approval=approval,
        attack_vector_desc=metadata["attack_vector_desc"],
        bts_url=metadata["bts_url"],
        compromised_attributes=metadata["compromised_attributes"],
        compromised_records=metadata["compromised_records"],
        creation=creation,
        cvss_version=metadata["cvss_version"],
        cwe=metadata["cwe"],
        description=metadata["description"],
        evidences=evidences,
        group_name=metadata["group_name"],
        id=metadata["id"],
        scenario=metadata["scenario"],
        severity=severity,
        sorts=FindingSorts[metadata["sorts"]],
        submission=submission,
        records=FindingRecords(**metadata["records"])
        if "records" in metadata
        else None,
        recommendation=metadata["recommendation"],
        requirements=metadata["requirements"],
        risk=metadata["risk"],
        title=metadata["title"],
        threat=metadata["threat"],
        type=metadata["type"],
        state=state,
        unreliable_indicators=unreliable_indicators,
        verification=verification,
    )


async def _get_finding(*, group_name: str, finding_id: str) -> Finding:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["finding_approval"],
            TABLE.facets["finding_creation"],
            TABLE.facets["finding_metadata"],
            TABLE.facets["finding_state"],
            TABLE.facets["finding_submission"],
            TABLE.facets["finding_unreliable_indicators"],
            TABLE.facets["finding_verification"],
        ),
        index=index,
        table=TABLE,
    )

    if not results:
        raise FindingNotFound()

    return _build_finding(
        item_id=primary_key.partition_key,
        key_structure=key_structure,
        raw_items=results,
    )


async def _get_group(*, finding_id: str) -> str:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_metadata"],),
        table=TABLE,
    )
    inverted_index = TABLE.indexes["inverted_index"]
    inverted_key_structure = inverted_index.primary_key
    metadata = historics.get_metadata(
        item_id=primary_key.partition_key,
        key_structure=inverted_key_structure,
        raw_items=results,
    )
    if not results:
        raise FindingNotFound()

    return metadata["group_name"]


async def _get_non_deleted_finding(*, finding_id: str) -> Finding:
    group_name = await _get_group(finding_id=finding_id)
    finding = await _get_finding(group_name=group_name, finding_id=finding_id)
    if finding.state.status == FindingStateStatus.DELETED:
        raise FindingNotFound
    return finding


async def _get_historic_verification(
    *, finding_id: str
) -> Tuple[FindingVerification, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_verification"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_verification"],),
        table=TABLE,
    )
    return tuple(map(format_verification, results))


async def _get_historic_state(*, finding_id: str) -> Tuple[FindingState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_state"],),
        table=TABLE,
    )
    return tuple(map(format_state, results))


class FindingNonDeletedNewLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Tuple[str, ...]
    ) -> Tuple[Finding, ...]:
        return await collect(
            _get_non_deleted_finding(finding_id=finding_id)
            for finding_id in finding_ids
        )


class FindingHistoricVerificationNewLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Tuple[str, ...]
    ) -> Tuple[Tuple[FindingVerification], ...]:
        return await collect(
            _get_historic_verification(finding_id=finding_id)
            for finding_id in finding_ids
        )


class FindingHistoricStateNewLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Tuple[str, ...]
    ) -> Tuple[Tuple[FindingState], ...]:
        return await collect(
            _get_historic_state(finding_id=finding_id)
            for finding_id in finding_ids
        )
