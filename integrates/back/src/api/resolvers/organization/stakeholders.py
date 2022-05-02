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
    Any,
    Dict,
    List,
)


@enforce_organization_level_auth_async
async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **kwargs: None
) -> List[Dict[str, Any]]:
    response: List[Dict[str, Any]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="organization",
        attr="stakeholders",
        id=parent["id"],
    )
    return response


async def resolve_no_cache(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, Any]]:
    org_id = parent["id"]
    organization_stakeholders_loader = (
        info.context.loaders.organization_stakeholders
    )
    org_stakeholders: List[
        Dict[str, Any]
    ] = await organization_stakeholders_loader.load(org_id)
    return org_stakeholders
