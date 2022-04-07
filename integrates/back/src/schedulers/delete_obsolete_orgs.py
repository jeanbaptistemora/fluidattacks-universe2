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
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)


async def _remove_group(
    loaders: Dataloaders,
    group_name: str,
    user_email: str,
) -> None:
    await groups_domain.remove_group_typed(
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
        queue="dedicated_later",
        product_name=Product.INTEGRATES,
    )


async def _remove_organization(
    loaders: Dataloaders, organization_id: str, email: str
) -> None:
    users = await orgs_domain.get_users(organization_id)
    users_removed = await collect(
        orgs_domain.remove_user(loaders, organization_id, user)
        for user in users
    )
    success = all(users_removed) if users else True

    org_groups = await orgs_domain.get_groups(organization_id)
    await collect(_remove_group(loaders, group, email) for group in org_groups)
    if success:
        await orgs_domain.remove_organization(organization_id)


async def delete_obsolete_orgs() -> None:
    """Delete obsolete organizations."""
    today = datetime_utils.get_now().date()
    email = "integrates@fluidattacks.com"
    loaders: Dataloaders = get_new_context()
    async for org_id, org_name in orgs_domain.iterate_organizations():
        org_pending_deletion_date_str = (
            await orgs_domain.get_pending_deletion_date_str(org_id)
        )
        org_users = await orgs_domain.get_users(org_id)
        org_groups = await orgs_domain.get_groups(org_id)
        if len(org_users) == 0 and len(org_groups) == 0:
            if org_pending_deletion_date_str:
                org_pending_deletion_date = datetime_utils.get_from_str(
                    org_pending_deletion_date_str
                )
                if org_pending_deletion_date.date() <= today:
                    await _remove_organization(loaders, org_id, email)
            else:
                new_org_pending_deletion_date_str = datetime_utils.get_as_str(
                    datetime_utils.get_now_plus_delta(days=60)
                )
                await orgs_domain.update_pending_deletion_date(
                    org_id, org_name, new_org_pending_deletion_date_str
                )
        else:
            await orgs_domain.update_pending_deletion_date(
                org_id, org_name, None
            )


async def main() -> None:
    await delete_obsolete_orgs()
