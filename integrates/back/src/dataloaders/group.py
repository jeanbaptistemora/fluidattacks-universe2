from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from db_model.groups.types import (
    Group,
    GroupState,
    GroupUnreliableIndicators,
)
from dynamodb.types import (
    Item,
)
from groups import (
    dal as groups_dal,
)
from newutils.groups import (
    format_group,
    format_group_historic_state,
    format_group_unreliable_indicators,
)
from organizations import (
    domain as orgs_domain,
)


class GroupTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: tuple[str, ...]
    ) -> tuple[Group, ...]:
        organization_ids = await collect(
            orgs_domain.get_id_for_group(group_name)
            for group_name in group_names
        )
        groups_items: list[Item] = await groups_dal.get_many_groups(
            list(group_names)
        )
        return tuple(
            format_group(
                item=group,
                organization_id=organization_id,
            )
            for group, organization_id in zip(groups_items, organization_ids)
        )


async def _get_organization_groups(organization_id: str) -> tuple[Group, ...]:
    group_names = await orgs_domain.get_groups(organization_id)
    group_items = await groups_dal.get_many_groups(list(group_names))
    return tuple(
        format_group(
            item=group,
            organization_id=organization_id,
        )
        for group in group_items
    )


class OrganizationGroupsTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_ids: tuple[str, ...]
    ) -> tuple[tuple[Group, ...], ...]:
        return await collect(
            tuple(map(_get_organization_groups, organization_ids))
        )


class GroupIndicatorsTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: tuple[str, ...]
    ) -> tuple[GroupUnreliableIndicators, ...]:
        groups_items: list[Item] = await groups_dal.get_groups_indicators(
            list(group_names)
        )
        return tuple(
            format_group_unreliable_indicators(item=item)
            for item in groups_items
        )


class GroupHistoricStateTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: tuple[str, ...]
    ) -> tuple[tuple[GroupState, ...], ...]:
        groups_items: list[Item] = await groups_dal.get_many_groups(
            list(group_names)
        )
        return tuple(
            format_group_historic_state(item=item) for item in groups_items
        )
