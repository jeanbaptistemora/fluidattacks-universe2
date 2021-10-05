from .enums import (
    FindingStateStatus,
)
from .types import (
    Finding,
    FindingState,
    FindingVerification,
)
from .utils import (
    filter_non_state_status_findings,
    format_finding,
    format_state,
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
from typing import (
    List,
    Tuple,
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

    return format_finding(
        item_id=primary_key.partition_key,
        key_structure=key_structure,
        raw_items=results,
    )


async def _get_findings_by_group(group_name: str) -> Tuple[Finding, ...]:
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
        format_finding(
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


async def _get_finding_by_id(finding_id: str) -> Finding:
    group_name = await _get_group(finding_id=finding_id)
    finding = await _get_finding(group_name=group_name, finding_id=finding_id)
    if finding.state.status == FindingStateStatus.DELETED:
        raise FindingNotFound()

    return finding


async def _get_historic_verification(
    finding_id: str,
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


async def _get_historic_state(finding_id: str) -> Tuple[FindingState, ...]:
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


class FindingNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Finding, ...]:
        return await collect(tuple(map(_get_finding_by_id, finding_ids)))


class FindingHistoricVerificationNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[FindingVerification], ...]:
        return await collect(
            tuple(map(_get_historic_verification, finding_ids))
        )


class FindingHistoricStateNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[FindingState], ...]:
        return await collect(tuple(map(_get_historic_state, finding_ids)))


class GroupDraftsNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        findings_by_group = await collect(
            tuple(map(_get_findings_by_group, group_names))
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
            tuple(map(_get_findings_by_group, group_names))
        )
        return tuple(
            filter_non_state_status_findings(
                findings,
                {
                    FindingStateStatus.CREATED,
                    FindingStateStatus.DELETED,
                    FindingStateStatus.REJECTED,
                    FindingStateStatus.SUBMITTED,
                },
            )
            for findings in findings_by_group
        )


async def _get_removed_findings_by_group(
    group_name: str,
) -> Tuple[Finding, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["removed_finding_metadata"],
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
        format_finding(
            item_id=finding_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for finding_id, items in finding_items.items()
    )


class GroupRemovedFindingsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        return await collect(
            tuple(map(_get_removed_findings_by_group, group_names))
        )
