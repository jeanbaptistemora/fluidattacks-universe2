from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.groups import (
    get_group_max_number_acceptances,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[int]:

    return await get_group_max_number_acceptances(
        loaders=info.context.loaders,
        group=parent,
    )
