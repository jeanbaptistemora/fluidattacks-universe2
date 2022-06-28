from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from newutils.stakeholders import (
    format_stakeholder,
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
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> List[Stakeholder]:
    response: List[Dict[str, Any]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="organization",
        attr="stakeholders",
        id=parent.id,
    )
    stakeholders: list[Stakeholder] = [
        format_stakeholder(item_legacy=stakeholder, item_vms=None)
        for stakeholder in response
    ]
    return stakeholders


async def resolve_no_cache(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[Dict[str, Any]]:
    org_id = parent.id
    organization_stakeholders_loader = (
        info.context.loaders.organization_stakeholders
    )
    org_stakeholders: List[
        Dict[str, Any]
    ] = await organization_stakeholders_loader.load(org_id)
    return org_stakeholders
