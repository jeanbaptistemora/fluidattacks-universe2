from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.get import (
    get_download_url,
)
from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@enforce_group_level_auth_async
async def resolve(parent: GitRoot, _: GraphQLResolveInfo) -> Optional[str]:
    if parent.state.status == RootStatus.INACTIVE:
        return None

    return await get_download_url(
        group_name=parent.group_name, root_nickname=parent.state.nickname
    )
