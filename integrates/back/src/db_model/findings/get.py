from .enums import (
    FindingCvssVersion,
    FindingSorts,
    FindingStateStatus,
)
from .types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingVerification,
)
from .utils import (
    filter_non_state_status_findings,
    format_optional_state,
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
from collections import (
    defaultdict,
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
from itertools import (
    chain,
)
from typing import (
    List,
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
    approval = format_optional_state(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="APPROVAL",
            raw_items=raw_items,
        )
    )
    creation = format_state(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="CREATION",
            raw_items=raw_items,
        )
    )
    submission = format_optional_state(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="SUBMISSION",
            raw_items=raw_items,
        )
    )
    verification = format_optional_verification(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="VERIFICATION",
            raw_items=raw_items,
        )
    )

    if metadata["cvss_version"] == FindingCvssVersion.V31.value:
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
        attack_vector_description=metadata["attack_vector_description"],
        bug_tracking_system_url=metadata["bug_tracking_system_url"],
        compromised_attributes=metadata["compromised_attributes"],
        compromised_records=int(metadata["compromised_records"]),
        creation=creation,
        description=metadata["description"],
        evidences=evidences,
        group_name=metadata["group_name"],
        id=metadata["id"],
        scenario=metadata["scenario"],
        severity=severity,
        sorts=FindingSorts[metadata["sorts"]],
        submission=submission,
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


async def _get_findings_by_group(*, group_name: str) -> Tuple[Finding, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
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
    finding_items = defaultdict(list)
    for item in results:
        finding_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        finding_items[finding_id].append(item)

    return tuple(
        _build_finding(
            item_id=finding_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for finding_id, items in finding_items.items()
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
    if not results:
        raise FindingNotFound()
    inverted_index = TABLE.indexes["inverted_index"]
    inverted_key_structure = inverted_index.primary_key
    metadata = historics.get_metadata(
        item_id=primary_key.partition_key,
        key_structure=inverted_key_structure,
        raw_items=results,
    )

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
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Finding, ...]:
        return await collect(
            _get_non_deleted_finding(finding_id=finding_id)
            for finding_id in finding_ids
        )


class FindingHistoricVerificationNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[FindingVerification], ...]:
        return await collect(
            _get_historic_verification(finding_id=finding_id)
            for finding_id in finding_ids
        )


class FindingHistoricStateNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[FindingState], ...]:
        return await collect(
            _get_historic_state(finding_id=finding_id)
            for finding_id in finding_ids
        )


class GroupDraftsNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        findings_by_group = await collect(
            _get_findings_by_group(group_name=group_name)
            for group_name in group_names
        )
        return tuple(
            filter_non_state_status_findings(
                findings,
                {
                    FindingStateStatus.APPROVED,
                    FindingStateStatus.DELETED,
                },
            )
            for findings in findings_by_group
        )


class GroupFindingsNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        findings_by_group = await collect(
            _get_findings_by_group(group_name=group_name)
            for group_name in group_names
        )
        return tuple(
            filter_non_state_status_findings(
                findings,
                {
                    FindingStateStatus.CREATED,
                    FindingStateStatus.REJECTED,
                    FindingStateStatus.SUBMITTED,
                },
            )
            for findings in findings_by_group
        )


class GroupFindingsNonDeletedNewLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super(GroupFindingsNonDeletedNewLoader, self).__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, group_names: List[str]
    ) -> Tuple[Finding, ...]:
        unchained_data = await self.load_many(group_names)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        findings_by_group = await self.dataloader.load_many(group_names)
        return tuple(
            filter_non_state_status_findings(
                findings,
                {
                    FindingStateStatus.DELETED,
                },
            )
            for findings in findings_by_group
        )
