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
from custom_exceptions import (
    FindingNotFound,
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
)


async def _get_finding_by_id(finding_id: str) -> Finding:
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
        raise FindingNotFound()

    return format_finding(response.items[0])


async def _get_me_drafts(*, user_email: str) -> tuple[Finding, ...]:
    primary_key = keys.build_key(
        facet=ME_DRAFTS_INDEX_METADATA,
        values={"email": user_email},
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

    return tuple(format_finding(item) for item in response.items)


async def _get_drafts_and_findings_by_group(
    group_name: str,
) -> tuple[Finding, ...]:
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

    return tuple(format_finding(item) for item in response.items)


class GroupDraftsAndFindingsLoader(DataLoader):
    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> tuple[Finding, ...]:
        unchained_data = await self.load_many(group_names)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[Finding, ...], ...]:
        return await collect(
            tuple(map(_get_drafts_and_findings_by_group, group_names))
        )


class MeDraftsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[Finding, ...]:
        return await collect(
            tuple(
                _get_me_drafts(user_email=user_email)  # type: ignore
                for user_email in emails
            )
        )


class GroupDraftsLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[Finding, ...], ...]:
        drafts_and_findings_by_groups = await self.dataloader.load_many(
            group_names
        )
        return tuple(
            filter_non_state_status_findings(
                drafts_and_findings,
                {
                    FindingStateStatus.APPROVED,
                    FindingStateStatus.DELETED,
                    FindingStateStatus.MASKED,
                },
            )
            for drafts_and_findings in drafts_and_findings_by_groups
        )


class GroupFindingsLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> tuple[Finding, ...]:
        unchained_data = await self.load_many(group_names)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[Finding, ...], ...]:
        drafts_and_findings_by_groups = await self.dataloader.load_many(
            group_names
        )
        return tuple(
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
            for drafts_and_findings in drafts_and_findings_by_groups
        )


class FindingLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> tuple[Finding, ...]:
        return await collect(tuple(map(_get_finding_by_id, finding_ids)))


async def _get_historic_verification(
    finding_id: str,
) -> tuple[FindingVerification, ...]:
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
    async def load_many_chained(
        self, finding_ids: Iterable[str]
    ) -> tuple[FindingVerification, ...]:
        unchained_data = await self.load_many(finding_ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> tuple[tuple[FindingVerification], ...]:
        return await collect(
            tuple(
                map(_get_historic_verification, finding_ids)  # type: ignore
            ),
            workers=32,
        )


async def _get_historic_state(finding_id: str) -> tuple[FindingState, ...]:
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
    async def load_many_chained(
        self, finding_ids: Iterable[str]
    ) -> tuple[FindingState, ...]:
        unchained_data = await self.load_many(finding_ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> tuple[tuple[FindingState], ...]:
        return await collect(
            tuple(
                map(
                    _get_historic_state,  # type: ignore
                    finding_ids,
                )
            )
        )
