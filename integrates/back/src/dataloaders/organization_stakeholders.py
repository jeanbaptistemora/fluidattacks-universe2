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
    Any,
    cast,
    Dict,
    List,
    Tuple,
)


async def _get_org_users(email: str, org_id: str) -> Dict[str, Any]:
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


async def get_stakeholders_by_organization(
    organization_id: str,
) -> Tuple[Dict[str, Any], ...]:
    org_stakeholders_emails: List[str] = await orgs_domain.get_users(
        organization_id
    )
    org_stakeholders = await collect(
        _get_org_users(email, organization_id)
        for email in org_stakeholders_emails
    )
    return tuple(org_stakeholders)


class OrganizationStakeholdersLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: List[str]
    ) -> Tuple[Tuple[Dict[str, Any], ...], ...]:
        return cast(
            Tuple[Tuple[Dict[str, Any], ...], ...],
            await collect(
                get_stakeholders_by_organization(organization_name)
                for organization_name in organization_names
            ),
        )
