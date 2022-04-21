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
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)


@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> Decimal:
    response: Decimal = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="max_severity",
        name=parent.name,
    )
    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    unreliable_indicators: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load(group_name)
    )

    return (
        unreliable_indicators.max_severity
        if unreliable_indicators.max_severity
        else await groups_domain.get_max_severity(loaders, group_name)
    )
