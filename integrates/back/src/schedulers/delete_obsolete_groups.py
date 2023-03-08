from aioextensions import (
    collect,
)
from collections.abc import (
    Iterable,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupStateJustification,
)
from db_model.groups.types import (
    Group,
)
from group_access.domain import (
    get_group_stakeholders,
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
from schedulers.common import (
    info,
)


async def _remove_group(
    loaders: Dataloaders,
    group_name: str,
    user_email: str,
) -> None:
    await groups_domain.remove_group(
        loaders=loaders,
        email=user_email,
        group_name=group_name,
        justification=GroupStateJustification.OTHER,
        validate_pending_actions=False,
    )


async def _remove_groups(
    loaders: Dataloaders,
    obsolete_groups: Iterable[Group],
    user_email: str,
) -> None:
    today = datetime_utils.get_utc_now().date()
    groups_to_remove = [
        group
        for group in obsolete_groups
        if (
            group.state.pending_deletion_date
            and group.state.pending_deletion_date.date() <= today
        )
    ]
    if groups_to_remove:
        await collect(
            [
                _remove_group(loaders, group.name, user_email)
                for group in groups_to_remove
            ]
        )
        groups_names_to_log = [group.name for group in groups_to_remove]
        info(f"Removed groups: {groups_names_to_log}")


async def _remove_group_pending_deletion_dates(
    active_groups: Iterable[Group],
    obsolete_groups: Iterable[Group],
    user_email: str,
) -> None:
    groups_to_remove_pending_deletion_date = [
        group
        for group in active_groups
        if (
            group.state.pending_deletion_date
            and group.name not in [group.name for group in obsolete_groups]
        )
    ]
    if groups_to_remove_pending_deletion_date:
        await collect(
            [
                groups_domain.remove_pending_deletion_date(
                    group=group,
                    modified_by=user_email,
                )
                for group in groups_to_remove_pending_deletion_date
            ]
        )
        groups_names_to_log = [
            group.name for group in groups_to_remove_pending_deletion_date
        ]
        info(f"Pending deletion date REMOVED for: {groups_names_to_log}")


async def _set_group_pending_deletion_dates(
    obsolete_groups: Iterable[Group],
    user_email: str,
) -> None:
    groups_to_set_pending_deletion_date = [
        group
        for group in obsolete_groups
        if not group.state.pending_deletion_date
    ]
    pending_deletion_date = datetime_utils.get_now_plus_delta(weeks=1)
    if groups_to_set_pending_deletion_date:
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
        groups_names_to_log = [
            group.name for group in groups_to_set_pending_deletion_date
        ]
        info(f"Pending deletion date SET for: {groups_names_to_log}")


async def delete_obsolete_groups() -> None:
    """
    Remove groups without users, findings nor Fluid Attacks services enabled.
    """
    loaders: Dataloaders = get_new_context()
    user_email = "integrates@fluidattacks.com"
    async for _, org_name, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        info(f"Working on organization {org_name}")
        if not org_groups_names:
            continue
        groups = await collect(
            [
                groups_domain.get_group(loaders, org_group_name)
                for org_group_name in org_groups_names
            ]
        )
        active_groups = groups_utils.filter_active_groups(groups)
        if not active_groups:
            continue
        info(f"Active groups for {org_name}: {len(active_groups)}")
        no_squad_groups = [
            group for group in active_groups if not group.state.has_squad
        ]
        no_squad_groups_names = [group.name for group in no_squad_groups]
        no_squad_groups_findings = await loaders.group_findings.load_many(
            no_squad_groups_names
        )
        no_squad_groups_stakeholders = [
            await get_group_stakeholders(loaders, group_name)
            for group_name in no_squad_groups_names
        ]
        obsolete_groups = [
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
        ]
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
