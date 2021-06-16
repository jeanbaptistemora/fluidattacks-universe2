from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from decorators import (
    require_integrates,
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


@require_integrates
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> float:
    response: float = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_severity",
        name=cast(str, parent["name"]),
    )
    return response


async def resolve_no_cache(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> float:
    group_findings_loader: DataLoader = info.context.loaders.group_findings
    group_name: str = cast(str, parent["name"])

    finding_loader: DataLoader = info.context.loaders.finding
    finding_ids: List[str] = [
        finding["id"]
        for finding in await group_findings_loader.load(group_name)
    ]
    findings = await finding_loader.load_many(finding_ids)

    max_severity: float = (
        max([finding["severity_score"] for finding in findings])
        if findings
        else 0
    )
    return max_severity
