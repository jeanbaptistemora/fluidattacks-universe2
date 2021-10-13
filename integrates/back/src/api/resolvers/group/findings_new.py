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
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    utils,
)
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: Any
) -> Tuple[Finding, ...]:
    group_findings_loader: DataLoader = info.context.loaders.group_findings_new
    group_name: str = parent["name"]
    filters: Optional[Dict[str, Any]] = kwargs.get("filters")
    findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    if filters:
        return await utils.filter_findings(findings, filters)

    return findings
