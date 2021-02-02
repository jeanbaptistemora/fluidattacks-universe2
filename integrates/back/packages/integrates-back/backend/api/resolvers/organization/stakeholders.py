# Standard libraries
from functools import partial
from typing import (
    cast,
    List
)

# Third party libraries
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import authz
from backend.dal.helpers.redis import redis_get_or_set_entity_attr
from backend.decorators import enforce_organization_level_auth_async
from backend.domain import (
    organization as org_domain,
    user as stakeholder_domain
)
from backend.typing import (
    Organization as OrganizationType,
    Stakeholder as StakeholderType
)


async def _get_stakeholder(email: str, org_id: str) -> StakeholderType:
    stakeholder: StakeholderType = await stakeholder_domain.get_by_email(email)
    org_role: str = await authz.get_organization_level_role(email, org_id)

    return {**stakeholder, 'responsibility': '', 'role': org_role}


@enforce_organization_level_auth_async
async def resolve(
    parent: OrganizationType,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> List[StakeholderType]:
    response: List[StakeholderType] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='organization',
        attr='stakeholders',
        id=cast(str, parent['id'])
    )

    return response


async def resolve_no_cache(
    parent: OrganizationType,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[StakeholderType]:
    org_id: str = cast(str, parent['id'])
    org_stakeholders: List[str] = await org_domain.get_users(org_id)

    return cast(
        List[StakeholderType],
        await collect(
            _get_stakeholder(email, org_id)
            for email in org_stakeholders
        )
    )
