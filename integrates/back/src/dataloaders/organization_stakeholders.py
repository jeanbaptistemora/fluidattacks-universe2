from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    StakeholderNotFound,
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


async def _get_stakeholder(
    stakeholder_loader: DataLoader, email: str
) -> Stakeholder:
    try:
        return await stakeholder_loader.load(email)
    except StakeholderNotFound:
        return Stakeholder(
            email=email,
            is_registered=False,
        )


async def get_organization_stakeholders(
    organization_id: str,
    stakeholder_loader: DataLoader,
) -> tuple[Stakeholder, ...]:
    stakeholders_emails: list[str] = await orgs_domain.get_users(
        organization_id
    )
    return await collect(
        tuple(
            _get_stakeholder(stakeholder_loader, email)
            for email in stakeholders_emails
        )
    )


class OrganizationStakeholdersLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> tuple[tuple[Stakeholder], ...]:
        return await collect(
            get_organization_stakeholders(organization_id, self.dataloader)
            for organization_id in organization_ids
        )
