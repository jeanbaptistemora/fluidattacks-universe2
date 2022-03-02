from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
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
    Optional,
    Tuple,
    Union,
)


@require_asm
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> Optional[Finding]:
    response: Optional[Finding] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_severity_finding",
        name=parent["name"] if isinstance(parent, dict) else parent.name,
    )
    return response


async def resolve_no_cache(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Finding]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
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
