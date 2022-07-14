from dataloaders import (
    Dataloaders,
)
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
from newutils import (
    token as token_utils,
)
from newutils.stakeholders import (
    format_stakeholder,
    format_stakeholder_item,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    Any,
)


@enforce_organization_level_auth_async
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> list[Stakeholder]:
    # The store is needed to resolve stakeholder's role
    request_store = token_utils.get_request_store(info.context)
    request_store["entity"] = "ORGANIZATION"
    request_store["organization_id"] = parent.id

    response: list[dict[str, Any]] = await redis_get_or_set_entity_attr(
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
) -> list[dict[str, Any]]:
    loaders: Dataloaders = info.context.loaders
    org_stakeholders: tuple[
        Stakeholder, ...
    ] = await loaders.organization_stakeholders.load(parent.id)
    org_stakeholders_item = [
        format_stakeholder_item(group_stakeholder)
        for group_stakeholder in org_stakeholders
    ]
    return org_stakeholders_item
