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
    GroupUnreliableIndicators,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("maxOpenSeverityFinding")
@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Finding | None:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    finding_id = group_indicators.last_closed_vulnerability_finding

    return await loaders.finding.load(finding_id) if finding_id else None
