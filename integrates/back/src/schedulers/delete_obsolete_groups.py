from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_types import (
    Group as GroupType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
    List,
    Tuple,
)


async def _delete_groups(
    loaders: Any, obsolete_groups: List[GroupType]
) -> bool:
    today = datetime_utils.get_now().date()
    email = "integrates@fluidattacks.com"
    groups_to_delete = [
        obsolete_group
        for obsolete_group in obsolete_groups
        if (
            obsolete_group.get("pending_deletion_date")
            and datetime_utils.get_from_str(
                obsolete_group["pending_deletion_date"]
            ).date()
            <= today
        )
    ]
    groups_to_delete_org_ids = await collect(
        [
            orgs_domain.get_id_for_group(get_key_or_fallback(group_to_delete))
            for group_to_delete in groups_to_delete
        ]
    )
    return all(
        await collect(
            [
                groups_domain.remove_group(
                    loaders, get_key_or_fallback(group), email, org_id
                )
                for group, org_id in zip(
                    groups_to_delete, groups_to_delete_org_ids
                )
            ]
        )
    )


async def _remove_group_pending_deletion_dates(
    groups: List[GroupType], obsolete_groups: List[GroupType]
) -> bool:
    groups_to_remove_pending_deletion_date = [
        group
        for group in groups
        if (
            group.get("pending_deletion_date") and group not in obsolete_groups
        )
    ]
    return all(
        await collect(
            [
                groups_domain.update_pending_deletion_date(
                    get_key_or_fallback(group), None
                )
                for group in groups_to_remove_pending_deletion_date
            ]
        )
    )


async def _set_group_pending_deletion_dates(
    obsolete_groups: List[GroupType],
) -> bool:
    group_pending_deletion_date_str = datetime_utils.get_as_str(
        datetime_utils.get_now_plus_delta(weeks=1)
    )
    groups_to_set_pending_deletion_date = [
        get_key_or_fallback(obsolete_group)
        for obsolete_group in obsolete_groups
        if not obsolete_group.get("pending_deletion_date")
    ]
    return all(
        await collect(
            [
                groups_domain.update_pending_deletion_date(
                    group_name, group_pending_deletion_date_str
                )
                for group_name in groups_to_set_pending_deletion_date
            ]
        )
    )


async def delete_obsolete_groups() -> None:
    """
    Delete groups without users, findings nor Fluid Attacks services enabled
    """
    loaders: Dataloaders = get_new_context()
    group_findings_loader: DataLoader = loaders.group_findings
    group_stakeholders_loader: DataLoader = loaders.group_stakeholders
    group_attributes = {
        "project_name",
        "project_status",
        "historic_configuration",
        "pending_deletion_date",
    }
    groups = await groups_domain.get_alive_groups(group_attributes)
    inactive_groups = [
        group for group in groups if not groups_utils.has_asm_services(group)
    ]
    inactive_group_names = [
        get_key_or_fallback(group) for group in inactive_groups
    ]
    inactive_groups_findings: Tuple[
        Finding, ...
    ] = await group_findings_loader.load_many(inactive_group_names)
    inactive_groups_stakeholders = await group_stakeholders_loader.load_many(
        inactive_group_names
    )
    obsolete_groups = [
        inactive_group
        for (
            inactive_group,
            inactive_group_findings,
            inactive_group_stakeholders,
        ) in zip(
            inactive_groups,
            inactive_groups_findings,
            inactive_groups_stakeholders,
        )
        if len(inactive_group_findings) == 0
        and len(inactive_group_stakeholders) <= 1
    ]
    await collect(
        [
            _remove_group_pending_deletion_dates(groups, obsolete_groups),
            _set_group_pending_deletion_dates(obsolete_groups),
            _delete_groups(loaders, obsolete_groups),
        ]
    )


async def main() -> None:
    await delete_obsolete_groups()
