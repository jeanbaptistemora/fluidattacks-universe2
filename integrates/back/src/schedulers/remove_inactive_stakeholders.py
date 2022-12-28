from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    info,
)

INACTIVITY_DAYS = 90


async def remove_stakeholder(
    email: str,
    modified_by: str,
    organization_id: str,
) -> None:
    await orgs_domain.remove_access(
        loaders=get_new_context(),
        email=email,
        modified_by=modified_by,
        organization_id=organization_id,
    )
    info("Inactive stakeholder removed", extra={"email": email})


async def remove_inactive_stakeholders() -> None:
    """
    Remove stakeholders if only have access to imamura,
    and there are no logins in the defined period.
    """
    modified_by = "integrates@fluidattacks.com"
    loaders: Dataloaders = get_new_context()
    org_name = "imamura"
    organization: Organization = await loaders.organization.load(org_name)
    org_stakeholders: tuple[
        Stakeholder, ...
    ] = await orgs_domain.get_stakeholders(loaders, organization.id)
    inactive_stakeholders = [
        stakeholder
        for stakeholder in org_stakeholders
        if (
            stakeholder.last_login_date
            and (
                datetime_utils.get_plus_delta(
                    stakeholder.last_login_date,
                    days=INACTIVITY_DAYS,
                )
                < datetime_utils.get_utc_now()
            )
        )
    ]
    inactive_stakeholder_orgs = [
        await loaders.stakeholder_organizations_access.load(
            inactive_stakeholder.email
        )
        for inactive_stakeholder in inactive_stakeholders
    ]
    stakeholders_to_remove = [
        inactive_stakeholder
        for inactive_stakeholder, orgs in zip(
            inactive_stakeholders, inactive_stakeholder_orgs
        )
        if len(orgs) == 1
    ]
    await collect(
        tuple(
            remove_stakeholder(
                email=stakeholder_to_remove.email,
                organization_id=organization.id,
                modified_by=modified_by,
            )
            for stakeholder_to_remove in stakeholders_to_remove
        ),
        workers=16,
    )
    info("Stakeholders processed", extra={"len": len(stakeholders_to_remove)})


async def main() -> None:
    await remove_inactive_stakeholders()
