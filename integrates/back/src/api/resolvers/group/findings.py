from .schema import (
    GROUP,
)
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
)


@GROUP.field("findings")
@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> list[Finding]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    filters: dict[str, Any] | None = kwargs.get("filters")
    findings = await loaders.group_findings.load(group_name)
    if filters:
        return utils.filter_findings(findings, filters)

    return findings
