from functools import partial
from typing import (
    List,
    Optional,
    cast,
)

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import (
    Finding,
    Project as Group,
)
from decorators import require_integrates
from redis_cluster.operations import redis_get_or_set_entity_attr


@require_integrates
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> Optional[Finding]:
    response: Optional[Finding] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_severity_finding",
        name=cast(str, parent["name"]),
    )
    return response


async def resolve_no_cache(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[Finding]:
    finding_loader: DataLoader = info.context.loaders.finding
    group_findings_loader: DataLoader = info.context.loaders.group_findings

    group_name: str = cast(str, parent["name"])
    finding_ids: List[str] = [
        finding["id"]
        for finding in await group_findings_loader.load(group_name)
    ]
    findings = await finding_loader.load_many(finding_ids)

    _, finding = (
        max([(finding["severity_score"], finding) for finding in findings])
        if findings
        else (0, None)
    )
    if finding:
        return cast(Finding, finding)
    return None
