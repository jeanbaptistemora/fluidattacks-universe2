from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
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
    Any,
    Dict,
    Tuple,
    Union,
)


@require_asm
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> Decimal:
    response: Decimal = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_severity",
        name=parent["name"] if isinstance(parent, dict) else parent.name,
    )
    return response


async def resolve_no_cache(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    loaders: Dataloaders = info.context.loaders
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
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
