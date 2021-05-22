from functools import partial
from typing import cast

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Project as Group
from decorators import require_integrates
from redis_cluster.operations import redis_get_or_set_entity_attr


@require_integrates
async def resolve(
    parent: Group, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, _info, **_kwargs),
        entity="group",
        attr="total_findings",
        name=cast(str, parent["name"]),
    )
    return response


async def resolve_no_cache(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    group_name: str = cast(str, parent["name"])
    group_findings_loader: DataLoader = info.context.loaders.group_findings
    return len(await group_findings_loader.load(group_name))
