# Standard
from typing import cast, List

# Third party
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz
from backend.decorators import enforce_organization_level_auth_async
from backend.domain import (
    organization as org_domain,
    user as stakeholder_domain
)
from backend.typing import Organization, Stakeholder


async def _get_stakeholder(email: str, org_id: str) -> Stakeholder:
    stakeholder: Stakeholder = await stakeholder_domain.get_by_email(email)
    org_role: str = await authz.get_organization_level_role(email, org_id)

    return {**stakeholder, 'responsibility': '', 'role': org_role}


@enforce_organization_level_auth_async
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Stakeholder]:
    org_id: str = cast(str, parent['id'])

    org_stakeholders: List[str] = await org_domain.get_users(org_id)

    return cast(
        List[Stakeholder],
        await collect(
            _get_stakeholder(email, org_id)
            for email in org_stakeholders
        )
    )
