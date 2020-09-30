# Standard
from typing import cast, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz
from backend.api.resolvers import user as old_resolver
from backend.decorators import enforce_organization_level_auth_async
from backend.domain import (
    organization as org_domain,
    user as stakeholder_domain
)
from backend.typing import Organization, Stakeholder
from backend.utils import aio


async def _get_stakeholder(email: str, org_id: str) -> Stakeholder:
    stakeholder: Stakeholder = await stakeholder_domain.get_by_email(email)
    org_role: str = await authz.get_organization_level_role(email, org_id)

    return {**stakeholder, 'responsibility': '', 'role': org_role}


@enforce_organization_level_auth_async
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Stakeholder]:
    org_id: str = cast(str, parent['id'])

    org_stakeholders: List[str] = await org_domain.get_users(org_id)

    # Temporary while migrating stakeholder resolvers
    return cast(
        List[Stakeholder],
        await aio.materialize(
            old_resolver.resolve_for_organization(
                info,
                'ORGANIZATION',
                user_email,
                organization_id=org_id,
                field_name='stakeholders'
            )
            for user_email in org_stakeholders
        )
    )
