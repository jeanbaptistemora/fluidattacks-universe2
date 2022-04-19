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
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    utils,
)
from typing import (
    Any,
    Optional,
)


@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> tuple[Finding, ...]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    filters: Optional[dict[str, Any]] = kwargs.get("filters")
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    if filters:
        return await utils.filter_findings(findings, filters)

    return findings
