from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
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
    Tuple,
)


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> Decimal:
    response: Decimal = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_severity",
        name=parent["name"],
    )
    return response


async def resolve_no_cache(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Decimal:
    group_findings_loader: DataLoader = info.context.loaders.group_findings
    group_name: str = parent["name"]
    findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    max_severity: Decimal = max(
        map(
            lambda finding: findings_domain.get_severity_score(
                finding.severity
            ),
            findings,
        ),
        default=Decimal("0.0"),
    )
    return max_severity
