from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders.stakeholder import (
    get_stakeholder,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Iterable,
)


async def _get_stakeholder(email: str) -> Stakeholder:
    try:
        stakeholder = await get_stakeholder(email=email)
    except StakeholderNotFound:
        stakeholder = Stakeholder(
            email=email,
            first_name="",
            last_name="",
            is_registered=False,
        )
    return stakeholder


async def get_organization_stakeholders(
    organization_id: str,
) -> tuple[Stakeholder, ...]:
    org_stakeholders_emails: list[str] = await orgs_domain.get_users(
        organization_id
    )
    org_stakeholders = await collect(
        _get_stakeholder(email) for email in org_stakeholders_emails
    )
    return tuple(org_stakeholders)


class OrganizationStakeholdersLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> tuple[tuple[Stakeholder, ...], ...]:
        return await collect(
            get_organization_stakeholders(organization_name)
            for organization_name in organization_names
        )
