from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.groups import (
    get_group_max_acceptance_severity,
)


@GROUP.field("maxAcceptanceSeverity")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:

    return await get_group_max_acceptance_severity(
        loaders=info.context.loaders,
        group=parent,
    )
