from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding,
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
    List,
    Optional,
)


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> Optional[Finding]:
    # pylint: disable=unsubscriptable-object
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
    # pylint: disable=unsubscriptable-object
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
