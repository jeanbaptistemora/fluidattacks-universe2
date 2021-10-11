from custom_types import (
    Organization as OrganizationType,
    Stakeholder as StakeholderType,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    cast,
    List,
)


@enforce_organization_level_auth_async
async def resolve(
    parent: OrganizationType, info: GraphQLResolveInfo, **kwargs: None
) -> List[StakeholderType]:
    response: List[StakeholderType] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="organization",
        attr="stakeholders",
        id=parent["id"],
    )
    return response


async def resolve_no_cache(
    parent: OrganizationType, info: GraphQLResolveInfo, **_kwargs: None
) -> List[StakeholderType]:
    org_id: str = parent["id"]
    organization_stakeholders_loader = (
        info.context.loaders.organization_stakeholders
    )
    org_stakeholders: List[str] = await organization_stakeholders_loader.load(
        org_id
    )
    return cast(List[StakeholderType], org_stakeholders)
