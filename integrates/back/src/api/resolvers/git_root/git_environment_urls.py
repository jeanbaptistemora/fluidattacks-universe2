from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo
) -> tuple[GitEnvironmentUrl, ...]:
    loaders: Dataloaders = info.context.loaders
    urls: tuple[
        GitEnvironmentUrl, ...
    ] = await loaders.git_environment_urls.load((parent.id))

    return tuple(url._replace(group_name=parent.group_name) for url in urls)
