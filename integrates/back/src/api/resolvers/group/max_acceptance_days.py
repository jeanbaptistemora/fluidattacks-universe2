from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.groups import (
    get_group_max_acceptance_days,
)


@GROUP.field("maxAcceptanceDays")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int | None:

    return await get_group_max_acceptance_days(
        loaders=info.context.loaders, group=parent
    )
