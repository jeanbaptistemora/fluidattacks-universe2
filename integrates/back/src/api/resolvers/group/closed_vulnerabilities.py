from dataloaders import (
    Dataloaders,
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
from typing import (
    Optional,
)


@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[int]:
    loaders: Dataloaders = info.context.loaders
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load(parent.name)
    )
    return group_indicators.closed_vulnerabilities
