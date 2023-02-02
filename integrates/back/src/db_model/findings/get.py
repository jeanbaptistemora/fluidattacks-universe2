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
from db_model import (
    TABLE,
)
from db_model.findings.constants import (
    ME_DRAFTS_INDEX_METADATA,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
)
from typing import (
    Iterable,
    Optional,
)


async def _get_finding_by_id(finding_id: str) -> Optional[Finding]:
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
        limit=1,
        table=TABLE,
    )

    if not response.items:
        return None

    return format_finding(response.items[0])


async def _get_me_drafts(*, email: str) -> list[Finding]:
    primary_key = keys.build_key(
        facet=ME_DRAFTS_INDEX_METADATA,
        values={"email": email},
    )

    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_metadata"],),
        index=index,
        table=TABLE,
    )

    return [format_finding(item) for item in response.items]


async def _get_drafts_and_findings_by_group(
    group_name: str,
) -> list[Finding]:
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
        facets=(TABLE.facets["finding_metadata"],),
        index=index,
        table=TABLE,
    )

    return [format_finding(item) for item in response.items]


class GroupDraftsAndFindingsLoader(DataLoader[str, list[Finding]]):
    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> list[Finding]:
        unchained_data = await self.load_many(group_names)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[Finding]]:
        return list(
            await collect(
                tuple(map(_get_drafts_and_findings_by_group, group_names))
            )
        )


class MeDraftsLoader(DataLoader[str, list[Finding]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> list[list[Finding]]:
        return list(
            await collect(
                tuple(_get_me_drafts(email=email) for email in emails)
            )
        )


class GroupDraftsLoader(DataLoader[str, list[Finding]]):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[Finding]]:
        drafts_and_findings_by_groups = await self.dataloader.load_many(
            group_names
        )
        return [
            list(
                filter_non_state_status_findings(
                    tuple(drafts_and_findings),
                    {
                        FindingStateStatus.APPROVED,
                        FindingStateStatus.DELETED,
                        FindingStateStatus.MASKED,
                    },
                )
            )
            for drafts_and_findings in drafts_and_findings_by_groups
        ]


class GroupFindingsLoader(DataLoader[str, list[Finding]]):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> list[Finding]:
        unchained_data = await self.load_many(group_names)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[Finding]]:
        drafts_and_findings_by_groups = await self.dataloader.load_many(
            group_names
        )
        return [
            list(
                filter_non_state_status_findings(
                    drafts_and_findings,
                    {
                        FindingStateStatus.CREATED,
                        FindingStateStatus.DELETED,
                        FindingStateStatus.MASKED,
                        FindingStateStatus.REJECTED,
                        FindingStateStatus.SUBMITTED,
                    },
                )
            )
            for drafts_and_findings in drafts_and_findings_by_groups
        ]


class FindingLoader(DataLoader[str, Optional[Finding]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> list[Optional[Finding]]:
        return list(
            await collect(
                tuple(_get_finding_by_id(find_id) for find_id in finding_ids)
            )
        )


async def _get_historic_verification(
    finding_id: str,
) -> list[FindingVerification]:
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

    return list(map(format_verification, response.items))


class FindingHistoricVerificationLoader(
    DataLoader[str, list[FindingVerification]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> list[list[FindingVerification]]:
        return list(
            await collect(
                tuple(map(_get_historic_verification, finding_ids)),
                workers=32,
            )
        )


async def _get_historic_state(finding_id: str) -> list[FindingState]:
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

    return list(map(format_state, response.items))


class FindingHistoricStateLoader(DataLoader[str, list[FindingState]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> list[list[FindingState]]:
        return list(
            await collect(tuple(map(_get_historic_state, finding_ids)))
        )
