from .schema import (
    GROUP,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("compliance")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> GroupUnreliableIndicators:
    loaders: Dataloaders = info.context.loaders
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(parent.name)
    )
    return group_indicators
