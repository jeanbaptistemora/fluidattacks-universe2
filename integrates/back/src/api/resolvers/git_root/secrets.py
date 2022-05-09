from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    URLRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Union,
)


async def resolve(
    parent: Union[GitRoot, URLRoot], info: GraphQLResolveInfo
) -> str:
    loaders: Dataloaders = info.context.loaders
    return await loaders.root_secrets.load((parent.id))
