from .types import (
    Group,
    GroupState,
    GroupUnreliableIndicators,
)
from .utils import (
    format_group,
    format_state,
    format_unreliable_indicators,
    remove_org_id_prefix,
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
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_group(*, group_name: str) -> Group:
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

    return format_group(response.items[0])


async def _get_group_historic_state(
    *,
    group_name: str,
) -> tuple[GroupState, ...]:
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
    return tuple(map(format_state, response.items))


async def _get_group_unreliable_indicators(
    *, group_name: str
) -> GroupUnreliableIndicators:
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
        return GroupUnreliableIndicators()

    return format_unreliable_indicators(item)


async def _get_organization_groups(organization_id: str) -> tuple[Group, ...]:
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

    return tuple(format_group(item) for item in response.items)


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
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> tuple[tuple[Group, ...], ...]:
        return await collect(
            tuple(map(_get_organization_groups, organization_ids))
        )
