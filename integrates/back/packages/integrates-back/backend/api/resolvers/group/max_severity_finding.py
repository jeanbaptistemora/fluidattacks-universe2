# Standard
from functools import partial
from typing import (
    cast,
    List,
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
        attr='max_severity_finding',
        name=cast(str, parent['name']),
    )

    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Optional[Finding]:
    group_name: str = cast(str, parent['name'])

    group_findings_loader: DataLoader = info.context.loaders.group_findings
    finding_ids: List[str] = [
        finding['id']
        for finding in await group_findings_loader.load(group_name)
    ]

    finding_loader: DataLoader = info.context.loaders.finding
    findings = await finding_loader.load_many(finding_ids)

    _, finding = max([
        (finding['severity_score'], finding)
        for finding in findings
    ]) if findings else (0, None)

    if finding:
        return cast(Finding, finding)

    return None
