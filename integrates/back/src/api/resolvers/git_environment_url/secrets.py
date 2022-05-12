from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    Secret,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@enforce_group_level_auth_async
async def resolve(
    parent: GitEnvironmentUrl, info: GraphQLResolveInfo, **__: None
) -> tuple[Secret, ...]:
    loaders: Dataloaders = info.context.loaders
    return await loaders.environment_secrets.load((parent.id))
