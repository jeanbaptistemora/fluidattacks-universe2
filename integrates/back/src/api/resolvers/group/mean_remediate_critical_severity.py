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
    Any,
    Dict,
    Optional,
    Union,
)


@require_asm
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[int]:
    if isinstance(parent, dict):
        return parent["mean_remediate_critical_severity"]

    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load(group_name)
    )
    return group_indicators.mean_remediate_critical_severity
