from db_model.roots.get import (
    get_upload_url,
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
    return await get_upload_url(
        group_name=parent.group_name, root_nickname=parent.state.nickname
    )
