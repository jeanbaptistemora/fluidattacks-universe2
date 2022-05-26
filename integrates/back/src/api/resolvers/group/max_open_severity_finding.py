from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
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
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> Optional[Finding]:
    response: Optional[Finding] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_open_severity_finding",
        name=parent.name,
    )
    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Finding]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    finding_id = group_indicators.last_closed_vulnerability_finding

    return await loaders.finding.load(finding_id) if finding_id else None
