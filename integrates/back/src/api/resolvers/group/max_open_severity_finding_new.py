from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from db_model.findings.types import (
    Finding,
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
    Optional,
)


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> Optional[Finding]:
    response: Optional[Finding] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_open_severity_finding",
        name=parent["name"],
    )
    return response


async def resolve_no_cache(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[Finding]:
    finding_id: str = parent["max_open_severity_finding"]
    max_open_severity_finding: Optional[Finding] = None
    if finding_id:
        finding_loader: DataLoader = info.context.loaders.finding
        max_open_severity_finding = await finding_loader.load(finding_id)

    return max_open_severity_finding
