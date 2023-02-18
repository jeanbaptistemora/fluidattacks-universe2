from .schema import (
    GIT_ROOT,
)
from db_model.roots.get import (
    get_upload_url,
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


@GIT_ROOT.field("uploadUrl")
@enforce_group_level_auth_async
async def resolve(parent: GitRoot, _: GraphQLResolveInfo) -> Optional[str]:
    return await get_upload_url(
        group_name=parent.group_name, root_nickname=parent.state.nickname
    )
