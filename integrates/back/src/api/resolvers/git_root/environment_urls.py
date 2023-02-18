from .schema import (
    GIT_ROOT,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    RootEnvironmentUrlType,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("environmentUrls")
async def resolve(parent: GitRoot, info: GraphQLResolveInfo) -> list[str]:
    loaders: Dataloaders = info.context.loaders
    urls = await loaders.root_environment_urls.load(parent.id)
    return list(
        {url.url for url in urls if url.url_type == RootEnvironmentUrlType.URL}
    )
