from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    organizations as orgs_model,
    stakeholders as stakeholders_model,
)
from db_model.constants import (
    DEFAULT_INACTIVITY_PERIOD,
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
from stakeholders import (
    domain as stakeholders_domain,
)


def _get_last_activity(stakeholder: Stakeholder) -> datetime:
    last_login_date = (
        stakeholder.last_login_date
        if stakeholder.last_login_date is not None
        else datetime.fromisoformat(datetime_utils.DEFAULT_ISO_STR)
    )

    last_api_token_use_date = (
        stakeholder.last_api_token_use_date
        if stakeholder.last_api_token_use_date is not None
        else datetime.fromisoformat(datetime_utils.DEFAULT_ISO_STR)
    )

    return max([last_login_date, last_api_token_use_date])


async def process_stakeholder(
    stakeholder: Stakeholder,
) -> None:
    if stakeholder.last_login_date is None:
        return

    loaders: Dataloaders = get_new_context()
    has_orgs = bool(
        await loaders.stakeholder_organizations_access.load(stakeholder.email)
    )
    if has_orgs:
        return

    inactivity_days = (
        datetime_utils.get_utc_now() - _get_last_activity(stakeholder)
    ).days
    if inactivity_days < DEFAULT_INACTIVITY_PERIOD:
        return

    await stakeholders_domain.remove(stakeholder.email)
    info(
        "Inactive stakeholder removed",
        extra={
            "email": stakeholder.email,
            "inactivity_days": inactivity_days,
            "last_login_date": stakeholder.last_login_date,
            "last_api_token_use_date": stakeholder.last_api_token_use_date,
        },
    )


async def process_organization(
    organization: Organization,
) -> None:
    loaders: Dataloaders = get_new_context()
    inactivity_period_policy = (
        organization.policies.inactivity_period or DEFAULT_INACTIVITY_PERIOD
    )
    org_stakeholders = await orgs_domain.get_stakeholders(
        loaders=loaders, organization_id=organization.id
    )
    inactive_stakeholders = [
        stakeholder
        for stakeholder in org_stakeholders
        if stakeholder
        and stakeholder.last_login_date
        and (
            datetime_utils.get_utc_now() - _get_last_activity(stakeholder)
        ).days
        > inactivity_period_policy
    ]
    if not inactive_stakeholders:
        return

    await collect(
        tuple(
            orgs_domain.remove_access(
                organization_id=organization.id,
                email=stakeholder.email,
                modified_by=orgs_domain.EMAIL_INTEGRATES,
                send_reassignment_email=True,
            )
            for stakeholder in inactive_stakeholders
        ),
        workers=1,
    )
    info(
        "Organization processed",
        extra={
            "organization_id": organization.id,
            "inactivity_policy": inactivity_period_policy,
            "inactive_stakeholders": len(inactive_stakeholders),
        },
    )


async def remove_inactive_stakeholders() -> None:
    """
    Remove stakeholders for inactivity (no logins) in the defined period.
    """
    all_organizations = await orgs_model.get_all_organizations()
    info("Organizations to process", extra={"item": len(all_organizations)})
    await collect(
        tuple(
            process_organization(
                organization=organization,
            )
            for organization in all_organizations
        ),
        workers=1,
    )

    all_stakeholders = await stakeholders_model.get_all_stakeholders()
    info("Stakeholders to process", extra={"item": len(all_stakeholders)})
    await collect(
        tuple(
            process_stakeholder(
                stakeholder=stakeholder,
            )
            for stakeholder in all_stakeholders
        ),
        workers=1,
    )


async def main() -> None:
    await remove_inactive_stakeholders()
