from .schema import (
    GIT_ROOT,
)
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


@GIT_ROOT.field("gitEnvironmentUrls")
async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo
) -> list[RootEnvironmentUrl]:
    loaders: Dataloaders = info.context.loaders
    urls = await loaders.root_environment_urls.load(parent.id)

    return [url._replace(group_name=parent.group_name) for url in urls]
