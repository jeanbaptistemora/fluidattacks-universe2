from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    GitRoot,
)


async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo, **__: None
) -> str:
    loaders: Dataloaders = info.context.loaders
    return await loaders.git_environment_urls.load((parent.id))
