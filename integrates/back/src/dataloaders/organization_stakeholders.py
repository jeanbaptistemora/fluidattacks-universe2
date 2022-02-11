from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
import authz
from custom_types import (
    Stakeholder as StakeholderType,
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
from users import (
    domain as stakeholders_domain,
)


def get_invitation_state(
    invitation: Dict[str, Any], stakeholder: StakeholderType
) -> str:
    if invitation and not invitation["is_used"]:
        return "PENDING"
    if not stakeholder.get("is_registered", False):
        return "UNREGISTERED"
    return "CONFIRMED"


async def _get_stakeholder(email: str, org_id: str) -> StakeholderType:
    organization_access, stakeholder = await collect(
        (
            orgs_domain.get_user_access(org_id, email),
            stakeholders_domain.get_by_email(email),
        )
    )
    invitation = organization_access.get("invitation")
    invitation_state = get_invitation_state(invitation, stakeholder)
    if invitation_state == "PENDING":
        org_role = invitation["role"]
    else:
        org_role = await authz.get_organization_level_role(email, org_id)

    return {
        **stakeholder,
        "responsibility": "",
        "invitation_state": invitation_state,
        "role": org_role,
    }


async def get_stakeholders_by_organization(
    organization_id: str,
) -> Tuple[StakeholderType, ...]:
    org_stakeholders_emails: List[str] = await orgs_domain.get_users(
        organization_id
    )
    org_stakeholders = await collect(
        _get_stakeholder(email, organization_id)
        for email in org_stakeholders_emails
    )
    return tuple(org_stakeholders)


class OrganizationStakeholdersLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: List[str]
    ) -> Tuple[Tuple[StakeholderType, ...], ...]:
        return cast(
            Tuple[Tuple[StakeholderType, ...], ...],
            await collect(
                get_stakeholders_by_organization(organization_name)
                for organization_name in organization_names
            ),
        )
