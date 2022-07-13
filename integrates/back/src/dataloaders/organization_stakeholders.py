from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders.stakeholder import (
    get_stakeholder,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from newutils.stakeholders import (
    get_invitation_state,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Iterable,
)


async def _get_stakeholder(email: str, org_id: str) -> Stakeholder:
    try:
        organization_access, stakeholder = await collect(
            (
                orgs_domain.get_user_access(org_id, email),
                get_stakeholder(email=email),
            )
        )
    except StakeholderNotFound:
        organization_access = await orgs_domain.get_user_access(org_id, email)
        stakeholder = Stakeholder(
            email=email,
            first_name="",
            last_name="",
            is_registered=False,
        )

    invitation = organization_access.get("invitation")
    invitation_state = get_invitation_state(invitation, stakeholder)
    if invitation_state == "PENDING":
        org_role = invitation["role"]
    else:
        org_role = await authz.get_organization_level_role(email, org_id)

    stakeholder = stakeholder._replace(
        responsibility=None,
        invitation_state=invitation_state,
        role=org_role,
    )
    return stakeholder


async def get_organization_stakeholders(
    organization_id: str,
) -> tuple[Stakeholder, ...]:
    org_stakeholders_emails: list[str] = await orgs_domain.get_users(
        organization_id
    )
    org_stakeholders = await collect(
        _get_stakeholder(email, organization_id)
        for email in org_stakeholders_emails
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
