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
from findings import (
    domain as findings_domain,
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
    Tuple,
)


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> Optional[Finding]:
    response: Optional[Finding] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_severity_finding",
        name=parent["name"],
    )
    return response


async def resolve_no_cache(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[Finding]:
    group_findings_loader: DataLoader = info.context.loaders.group_findings
    group_name: str = parent["name"]
    findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    _, max_severity_finding = max(
        [
            (
                findings_domain.get_severity_score(finding.severity),
                finding,
            )
            for finding in findings
        ],
        default=(0, None),
    )
    return max_severity_finding
