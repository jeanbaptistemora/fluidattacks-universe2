from db_model.roots.get import (
    get_upload_url,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    GitRoot,
)


async def resolve(parent: GitRoot, _: GraphQLResolveInfo, **__: None) -> str:
    return await get_upload_url(
        group_name=parent.group_name, root_nickname=parent.nickname
    )
