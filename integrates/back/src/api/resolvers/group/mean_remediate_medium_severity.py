from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
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
) -> Optional[Decimal]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load(group_name)
    )
    return group_indicators.mean_remediate_medium_severity
