from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    Product,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupStateRemovalJustification,
)
from db_model.groups.types import (
    Group,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
)
from organizations import (
    domain as orgs_domain,
)


async def _remove_group(
    loaders: Dataloaders,
    group_name: str,
    user_email: str,
) -> None:
    await groups_domain.remove_group(
        loaders=loaders,
        group_name=group_name,
        justification=GroupStateRemovalJustification.OTHER,
        user_email=user_email,
    )
    await batch_dal.put_action(
        action=Action.REMOVE_GROUP_RESOURCES,
        entity=group_name,
        subject=user_email,
        additional_info="obsolete_groups",
        queue="dedicated_later",
        product_name=Product.INTEGRATES,
    )


async def _remove_groups(
    loaders: Dataloaders,
    obsolete_groups: tuple[Group, ...],
    user_email: str,
) -> None:
    today = datetime_utils.get_now().date()
    groups_to_delete = [
        group
        for group in obsolete_groups
        if (
            group.state.pending_deletion_date
            and datetime_utils.get_datetime_from_iso_str(
                group.state.pending_deletion_date
            ).date()
            <= today
        )
    ]
    await collect(
        [
            _remove_group(loaders, group.name, user_email)
            for group in groups_to_delete
        ]
    )


async def _remove_group_pending_deletion_dates(
    active_groups: tuple[Group, ...],
    obsolete_groups: tuple[Group, ...],
    user_email: str,
) -> None:
    groups_to_remove_pending_deletion_date = tuple(
        group
        for group in active_groups
        if (
            group.state.pending_deletion_date
            and group.name not in [group.name for group in obsolete_groups]
        )
    )
    await collect(
        [
            groups_domain.remove_pending_deletion_date(
                group=group,
                modified_by=user_email,
            )
            for group in groups_to_remove_pending_deletion_date
        ]
    )


async def _set_group_pending_deletion_dates(
    obsolete_groups: tuple[Group, ...],
    user_email: str,
) -> None:
    pending_deletion_date: str = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_now_plus_delta(weeks=1)
    )
    groups_to_set_pending_deletion_date = [
        group
        for group in obsolete_groups
        if not group.state.pending_deletion_date
    ]
    await collect(
        [
            groups_domain.set_pending_deletion_date(
                group=group,
                modified_by=user_email,
                pending_deletion_date=pending_deletion_date,
            )
            for group in groups_to_set_pending_deletion_date
        ]
    )


async def delete_obsolete_groups() -> None:
    """
    Remove groups without users, findings nor Fluid Attacks services enabled.
    """
    loaders: Dataloaders = get_new_context()
    group_findings_loader: DataLoader = loaders.group_findings
    group_stakeholders_loader: DataLoader = loaders.group_stakeholders
    user_email = "integrates@fluidattacks.com"
    async for _, _, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups()
    ):
        if not org_groups_names:
            continue
        groups = await loaders.group_typed.load_many(org_groups_names)
        active_groups = groups_utils.filter_active_groups(groups)
        if not active_groups:
            continue
        no_squad_groups = tuple(
            group for group in active_groups if not group.state.has_squad
        )
        no_squad_groups_names = tuple(group.name for group in no_squad_groups)
        no_squad_groups_findings = await group_findings_loader.load_many(
            no_squad_groups_names
        )
        no_squad_groups_stakeholders = (
            await group_stakeholders_loader.load_many(no_squad_groups_names)
        )
        obsolete_groups = tuple(
            no_squad_group
            for (
                no_squad_group,
                no_squad_group_findings,
                no_squad_group_stakeholders,
            ) in zip(
                no_squad_groups,
                no_squad_groups_findings,
                no_squad_groups_stakeholders,
            )
            if len(no_squad_group_findings) == 0
            and len(no_squad_group_stakeholders) <= 1
        )
        await collect(
            [
                _remove_group_pending_deletion_dates(
                    active_groups, obsolete_groups, user_email
                ),
                _set_group_pending_deletion_dates(obsolete_groups, user_email),
                _remove_groups(loaders, obsolete_groups, user_email),
            ]
        )


async def main() -> None:
    await delete_obsolete_groups()
