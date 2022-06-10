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
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)


async def delete_imamura_stakeholders() -> None:
    """
    Delete stakeholders if only have access to imamura,
    and there are no logins in the last 60 days
    """
    modified_by = "integrates@fluidattacks.com"
    loaders: Dataloaders = get_new_context()
    org_name = "imamura"
    organization: Organization = await loaders.organization.load(org_name)
    org_id = organization.id
    organization_stakeholders_loader = loaders.organization_stakeholders
    org_stakeholders = await organization_stakeholders_loader.load(org_id)
    inactive_stakeholders = [
        stakeholder
        for stakeholder in org_stakeholders
        if (
            stakeholder["last_login"]
            and (
                datetime_utils.get_plus_delta(
                    datetime_utils.get_from_str(stakeholder["last_login"]),
                    days=60,
                )
                < datetime_utils.get_now()
            )
        )
    ]
    inactive_stakeholder_orgs = await collect(
        [
            orgs_domain.get_user_organizations(inactive_stakeholder["email"])
            for inactive_stakeholder in inactive_stakeholders
        ]
    )
    stakeholders_to_delete = [
        inactive_stakeholder
        for inactive_stakeholder, orgs in zip(
            inactive_stakeholders, inactive_stakeholder_orgs
        )
        if len(orgs) == 1
    ]
    await collect(
        [
            orgs_domain.remove_user(
                loaders, org_id, stakeholder_to_delete["email"], modified_by
            )
            for stakeholder_to_delete in stakeholders_to_delete
        ]
    )


async def main() -> None:
    await delete_imamura_stakeholders()
