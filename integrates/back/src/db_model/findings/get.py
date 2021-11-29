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
from itertools import (
    chain,
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
    response = await operations.query(
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

    if not response.items:
        raise FindingNotFound()

    return format_finding(
        item_id=primary_key.partition_key,
        key_structure=key_structure,
        raw_items=response.items,
    )


async def _get_drafts_and_findings_by_group(
    group_name: str,
) -> Tuple[Finding, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
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
    for item in response.items:
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


class GroupDraftsAndFindingsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        return await collect(
            tuple(map(_get_drafts_and_findings_by_group, group_names))
        )


class GroupDraftsLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        drafts_and_findings_by_groups = await self.dataloader.load_many(
            group_names
        )
        return tuple(
            filter_non_state_status_findings(
                drafts_and_findings,
                {
                    FindingStateStatus.APPROVED,
                },
            )
            for drafts_and_findings in drafts_and_findings_by_groups
        )


class GroupFindingsLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
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
        drafts_and_findings_by_groups = await self.dataloader.load_many(
            group_names
        )
        return tuple(
            filter_non_state_status_findings(
                drafts_and_findings,
                {
                    FindingStateStatus.CREATED,
                    FindingStateStatus.REJECTED,
                    FindingStateStatus.SUBMITTED,
                },
            )
            for drafts_and_findings in drafts_and_findings_by_groups
        )


async def _get_group(*, finding_id: str) -> str:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_metadata"],),
        table=TABLE,
    )
    if not response.items:
        raise FindingNotFound()
    inverted_index = TABLE.indexes["inverted_index"]
    inverted_key_structure = inverted_index.primary_key
    metadata = historics.get_metadata(
        item_id=primary_key.partition_key,
        key_structure=inverted_key_structure,
        raw_items=response.items,
    )

    return metadata["group_name"]


async def _get_finding_by_id(finding_id: str) -> Finding:
    group_name = await _get_group(finding_id=finding_id)
    finding = await _get_finding(group_name=group_name, finding_id=finding_id)

    return finding


class FindingLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Finding, ...]:
        return await collect(tuple(map(_get_finding_by_id, finding_ids)))


async def _get_historic_verification(
    finding_id: str,
) -> Tuple[FindingVerification, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_verification"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_verification"],),
        table=TABLE,
    )
    return tuple(map(format_verification, response.items))


class FindingHistoricVerificationLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[FindingVerification], ...]:
        return await collect(
            tuple(map(_get_historic_verification, finding_ids))
        )


async def _get_historic_state(finding_id: str) -> Tuple[FindingState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_state"],),
        table=TABLE,
    )
    return tuple(map(format_state, response.items))


class FindingHistoricStateLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[FindingState], ...]:
        return await collect(tuple(map(_get_historic_state, finding_ids)))


async def _get_removed_findings_by_group(
    group_name: str,
) -> Tuple[Finding, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["removed_finding_metadata"],
        values={"group_name": group_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
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
    for item in response.items:
        finding_id = "#".join(item[key_structure.sort_key].split("#")[:3])
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
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Finding, ...], ...]:
        return await collect(
            tuple(map(_get_removed_findings_by_group, group_names))
        )
