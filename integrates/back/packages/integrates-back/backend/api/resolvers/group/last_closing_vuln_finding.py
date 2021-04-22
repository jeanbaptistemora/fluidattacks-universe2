# Standard
from functools import partial
from typing import (
    cast,
    Optional,
)

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import require_integrates
from backend.typing import Finding, Project as Group
from redis_cluster.operations import redis_get_or_set_entity_attr


@require_integrates
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> Optional[Finding]:
    response: Optional[Finding] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='group',
        attr='last_closing_vuln_finding',
        name=cast(str, parent['name']),
    )

    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Optional[Finding]:
    finding_id: str = cast(str, parent['last_closing_vuln_finding'])

    if finding_id:
        finding_loader: DataLoader = info.context.loaders.finding
        finding: Finding = await finding_loader.load(finding_id)

        return finding

    return None
