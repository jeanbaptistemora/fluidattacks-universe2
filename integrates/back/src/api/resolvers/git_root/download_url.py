from db_model.roots.get import (
    get_download_url,
)
from db_model.roots.types import (
    GitRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(parent: GitRootItem, _: GraphQLResolveInfo) -> Optional[str]:
    if parent.state.status == "INACTIVE":
        return None

    return await get_download_url(
        group_name=parent.group_name, root_nickname=parent.state.nickname
    )
