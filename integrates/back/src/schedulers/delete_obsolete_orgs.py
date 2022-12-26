from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupStateJustification,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    OrganizationState,
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
        email=user_email,
        group_name=group_name,
        justification=GroupStateJustification.OTHER,
        validate_pending_actions=False,
    )


async def _remove_organization(
    loaders: Dataloaders,
    organization_id: str,
    organization_name: str,
    modified_by: str,
) -> None:
    group_names = await orgs_domain.get_group_names(loaders, organization_id)
    await collect(
        _remove_group(loaders, group, modified_by) for group in group_names
    )
    await orgs_domain.remove_organization(
        loaders=loaders,
        organization_id=organization_id,
        organization_name=organization_name,
        modified_by=modified_by,
    )
    info(
        f"Organization removed {organization_name}, "
        f"groups removed: {group_names}"
    )


async def delete_obsolete_orgs() -> None:
    """Remove obsolete organizations."""
    today = datetime_utils.get_utc_now()
    modified_by = "integrates@fluidattacks.com"
    loaders: Dataloaders = get_new_context()
    async for organization in orgs_domain.iterate_organizations():
        if orgs_utils.is_deleted(organization):
            continue

        info(f"Working on organization {organization.name}")
        org_pending_deletion_date = organization.state.pending_deletion_date
        org_group_names = await orgs_domain.get_group_names(
            loaders, organization.id
        )
        if len(org_group_names) == 0:
            if org_pending_deletion_date:
                if org_pending_deletion_date.date() <= today.date():
                    await _remove_organization(
                        loaders,
                        organization.id,
                        organization.name,
                        modified_by,
                    )
            else:
                new_deletion_date = datetime_utils.get_now_plus_delta(days=60)
                await orgs_domain.update_state(
                    organization_id=organization.id,
                    organization_name=organization.name,
                    state=OrganizationState(
                        modified_by=modified_by,
                        modified_date=datetime_utils.get_utc_now(),
                        status=organization.state.status,
                        pending_deletion_date=new_deletion_date,
                    ),
                )
                info(
                    f"Organization {organization.name} is set for deletion, "
                    f"date: {new_deletion_date}"
                )
        else:
            await orgs_domain.update_state(
                organization_id=organization.id,
                organization_name=organization.name,
                state=OrganizationState(
                    modified_by=modified_by,
                    modified_date=datetime_utils.get_utc_now(),
                    status=OrganizationStateStatus.ACTIVE,
                    pending_deletion_date=None,
                ),
            )


async def main() -> None:
    await delete_obsolete_orgs()
