from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    domain as roots_domain,
)
from roots.types import (
    GitRoot,
)


async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return await roots_domain.get_last_status_update(
        info.context.loaders, parent.id
    )
