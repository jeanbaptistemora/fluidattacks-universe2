from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from decorators import (
    require_asm,
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
)


@require_asm
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
