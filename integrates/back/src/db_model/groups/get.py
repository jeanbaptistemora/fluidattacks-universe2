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
from collections.abc import (
    Iterable,
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


async def _get_group(*, group_name: str) -> Group | None:
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
        return None

    return format_group(response.items[0])


class GroupLoader(DataLoader[str, Group | None]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[Group | None]:
        return list(
            await collect(
                tuple(
                    _get_group(group_name=group_name)
                    for group_name in group_names
                )
            )
        )


async def _get_group_historic_state(
    *,
    group_name: str,
) -> list[GroupState]:
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

    return list(map(format_state, response.items))


class GroupHistoricStateLoader(DataLoader[str, list[GroupState]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[GroupState]]:
        return list(
            await collect(
                tuple(
                    _get_group_historic_state(group_name=group_name)
                    for group_name in group_names
                )
            )
        )


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


class GroupUnreliableIndicatorsLoader(
    DataLoader[str, GroupUnreliableIndicators]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[GroupUnreliableIndicators]:
        return list(
            await collect(
                tuple(
                    _get_group_unreliable_indicators(group_name=group_name)
                    for group_name in group_names
                )
            )
        )


async def _get_organization_groups(
    *,
    group_dataloader: GroupLoader,
    organization_id: str,
) -> list[Group]:
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

    return groups


class OrganizationGroupsLoader(DataLoader[str, list[Group]]):
    def __init__(self, dataloader: GroupLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> list[list[Group]]:
        return list(
            await collect(
                tuple(
                    _get_organization_groups(
                        group_dataloader=self.dataloader,
                        organization_id=organization_id,
                    )
                    for organization_id in organization_ids
                )
            )
        )
