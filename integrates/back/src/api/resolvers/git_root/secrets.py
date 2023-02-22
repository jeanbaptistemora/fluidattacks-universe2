from .schema import (
    GIT_ROOT,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    Secret,
    URLRoot,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("secrets")
@enforce_group_level_auth_async
async def resolve(
    parent: GitRoot | URLRoot, info: GraphQLResolveInfo
) -> list[Secret]:
    loaders: Dataloaders = info.context.loaders
    return await loaders.root_secrets.load(parent.id)
