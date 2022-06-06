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
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
    organizations as orgs_utils,
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
        group_name=group_name,
        justification=GroupStateRemovalJustification.OTHER,
        user_email=user_email,
    )
    await batch_dal.put_action(
        action=Action.REMOVE_GROUP_RESOURCES,
        entity=group_name,
        subject=user_email,
        additional_info="obsolete_orgs",
        queue="small",
        product_name=Product.INTEGRATES,
    )


async def _remove_organization(
    loaders: Dataloaders,
    organization_id: str,
    organization_name: str,
    modified_by: str,
) -> None:
    users = await orgs_domain.get_users(organization_id)
    users_removed = await collect(
        orgs_domain.remove_user(loaders, organization_id, user)
        for user in users
    )
    success = all(users_removed) if users else True

    group_names = await orgs_domain.get_group_names(loaders, organization_id)
    await collect(
        _remove_group(loaders, group, modified_by) for group in group_names
    )
    if success:
        await orgs_domain.update_state(
            loaders,
            organization_id,
            modified_by,
            OrganizationStateStatus.DELETED,
        )
        info(
            f"Organization removed {organization_name}, "
            f"groups removed: {group_names}"
        )


async def delete_obsolete_orgs() -> None:
    """Remove obsolete organizations."""
    today = datetime_utils.get_now().date()
    modified_by = "integrates@fluidattacks.com"
    loaders: Dataloaders = get_new_context()
    async for organization in orgs_domain.iterate_organizations():
        if orgs_utils.is_deleted_typed(organization):
            continue

        info(f"Working on organization {organization.name}")
        org_pending_deletion_date_str = (
            organization.state.pending_deletion_date
        )
        org_users = await orgs_domain.get_users(organization.id)
        org_group_names = await orgs_domain.get_group_names(
            loaders, organization.id
        )
        if len(org_users) == 0 and len(org_group_names) == 0:
            if org_pending_deletion_date_str:
                org_pending_deletion_date = (
                    datetime_utils.get_datetime_from_iso_str(
                        org_pending_deletion_date_str
                    )
                )
                if org_pending_deletion_date.date() <= today:
                    await _remove_organization(
                        loaders,
                        organization.id,
                        organization.name,
                        modified_by,
                    )
            else:
                new_org_pending_deletion_date_str = datetime_utils.get_as_str(
                    datetime_utils.get_now_plus_delta(days=60)
                )
                await orgs_domain.update_pending_deletion_date(
                    organization.id,
                    organization.name,
                    new_org_pending_deletion_date_str,
                )
                info(
                    f"Organization {organization.name} is set for deletion, "
                    f"date: {new_org_pending_deletion_date_str}"
                )
        else:
            await orgs_domain.update_pending_deletion_date(
                organization.id, organization.name, None
            )


async def main() -> None:
    await delete_obsolete_orgs()
