from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(parent: GitRoot, info: GraphQLResolveInfo) -> str:
    loaders: Dataloaders = info.context.loaders
    return await loaders.git_environment_urls.load((parent.id))
