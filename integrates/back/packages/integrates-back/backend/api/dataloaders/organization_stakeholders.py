# Standard libraries
from typing import (
    cast,
    List,
    Tuple,
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend import authz
from backend.typing import Stakeholder as StakeholderType
from organizations import domain as orgs_domain
from users import domain as stakeholders_domain


async def _get_stakeholder(email: str, org_id: str) -> StakeholderType:
    stakeholder: StakeholderType = await stakeholders_domain.get_by_email(
        email
    )
    org_role: str = await authz.get_organization_level_role(email, org_id)

    return {**stakeholder, 'responsibility': '', 'role': org_role}


async def get_stakeholders_by_organization(
    organization_id: str
) -> Tuple[StakeholderType, ...]:
    org_stakeholders_emails: List[str] = \
        await orgs_domain.get_users(organization_id)
    org_stakeholders = await collect(
        _get_stakeholder(email, organization_id)
        for email in org_stakeholders_emails
    )

    return tuple(org_stakeholders)


class OrganizationStakeholdersLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        organization_names: List[str]
    ) -> Tuple[Tuple[StakeholderType, ...], ...]:
        return cast(
            Tuple[Tuple[StakeholderType, ...], ...],
            await collect(
                get_stakeholders_by_organization(organization_name)
                for organization_name in organization_names
            )
        )
