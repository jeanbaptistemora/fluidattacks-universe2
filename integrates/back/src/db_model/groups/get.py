# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    Group,
    GroupState,
    GroupUnreliableIndicators,
)
from .utils import (
    format_group,
    format_state,
    format_unreliable_indicators,
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
    GroupNotFound,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Iterable,
)


async def get_group_item(*, group_name: str) -> Item:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_metadata"],),
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise GroupNotFound()

    return response.items[0]


async def _get_group(*, group_name: str) -> Group:
    return format_group(await get_group_item(group_name=group_name))


async def get_group_historic_state_items(
    *,
    group_name: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_historic_state"],
        values={"name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_historic_state"],),
        table=TABLE,
    )
    return tuple(response.items)


async def _get_group_historic_state(
    *,
    group_name: str,
) -> tuple[GroupState, ...]:
    return tuple(
        map(
            format_state,
            await get_group_historic_state_items(group_name=group_name),
        )
    )


async def get_group_unreliable_indicators_item(*, group_name: str) -> Item:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_unreliable_indicators"],
        values={"name": group_name},
    )
    item = await operations.get_item(
        facets=(TABLE.facets["group_unreliable_indicators"],),
        key=primary_key,
        table=TABLE,
    )
    if not item:
        return {}

    return item


async def _get_group_unreliable_indicators(
    *, group_name: str
) -> GroupUnreliableIndicators:
    item = await get_group_unreliable_indicators_item(group_name=group_name)
    if not item:
        return GroupUnreliableIndicators()

    return format_unreliable_indicators(item)


async def _get_organization_groups(
    *,
    group_dataloader: DataLoader,
    organization_id: str,
) -> tuple[Group, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"organization_id": remove_org_id_prefix(organization_id)},
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
        facets=(TABLE.facets["group_metadata"],),
        table=TABLE,
        index=index,
    )

    groups: list[Group] = []
    for item in response.items:
        group = format_group(item)
        groups.append(group)
        group_dataloader.prime(group.name, group)

    return tuple(groups)


class GroupLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[Group, ...]:
        return await collect(
            tuple(
                _get_group(group_name=group_name) for group_name in group_names
            )
        )


class GroupHistoricStateLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[GroupState, ...], ...]:
        return await collect(
            tuple(
                _get_group_historic_state(group_name=group_name)
                for group_name in group_names
            )
        )


class GroupUnreliableIndicatorsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[GroupUnreliableIndicators, ...]:
        return await collect(
            tuple(
                _get_group_unreliable_indicators(group_name=group_name)
                for group_name in group_names
            )
        )


class OrganizationGroupsLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> tuple[tuple[Group, ...], ...]:
        return await collect(
            tuple(
                _get_organization_groups(
                    group_dataloader=self.dataloader,
                    organization_id=organization_id,
                )
                for organization_id in organization_ids
            )
        )
