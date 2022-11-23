from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    RootEnvironmentUrl,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo
) -> tuple[RootEnvironmentUrl, ...]:
    loaders: Dataloaders = info.context.loaders
    urls: tuple[
        RootEnvironmentUrl, ...
    ] = await loaders.root_environment_urls.load((parent.id))

    return tuple(url._replace(group_name=parent.group_name) for url in urls)
