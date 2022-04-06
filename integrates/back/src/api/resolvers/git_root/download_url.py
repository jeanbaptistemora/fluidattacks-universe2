from db_model.roots.get import (
    get_download_url,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    GitRoot,
)
from typing import (
    Optional,
)


async def resolve(
    parent: GitRoot, _: GraphQLResolveInfo, **__: None
) -> Optional[str]:
    if parent.state == "INACTIVE":
        return None

    return await get_download_url(
        group_name=parent.group_name, root_nickname=parent.nickname
    )
