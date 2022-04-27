from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: GitEnvironmentUrl, info: GraphQLResolveInfo, **__: None
) -> str:
    loaders: Dataloaders = info.context.loaders
    return await loaders.environment_secrets.load((parent.id))
