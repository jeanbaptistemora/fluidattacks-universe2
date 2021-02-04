# Standard
from functools import (
    partial,
)
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.decorators import (
    require_integrates,
)
from backend.typing import Project as Group


@require_integrates
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> float:
    response: float = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='group',
        attr='max_severity',
        name=cast(str, parent['name']),
    )

    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> float:
    group_name: str = cast(str, parent['name'])

    group_findings_loader: DataLoader = info.context.loaders.group_findings
    finding_ids: List[str] = [
        finding['id']
        for finding in await group_findings_loader.load(group_name)
    ]

    finding_loader: DataLoader = info.context.loaders.finding
    findings = await finding_loader.load_many(finding_ids)

    max_severity: float = max([
        finding['severity_score']
        for finding in findings
    ]) if findings else 0

    return max_severity
