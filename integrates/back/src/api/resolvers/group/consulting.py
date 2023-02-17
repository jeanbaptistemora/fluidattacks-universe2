from .schema import (
    GROUP,
)
from db_model.group_comments.types import (
    GroupComment,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_squad,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_comments import (
    domain as group_comments_domain,
)
from newutils.group_comments import (
    format_group_consulting_resolve,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@GROUP.field("consulting")
@concurrent_decorators(
    enforce_group_level_auth_async, require_asm, require_squad
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, Any]]:
    user_data: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    group_comments: tuple[
        GroupComment, ...
    ] = await group_comments_domain.get_comments(
        loaders=info.context.loaders,
        group_name=parent.name,
        email=user_data["user_email"],
    )

    return [
        format_group_consulting_resolve(comment) for comment in group_comments
    ]
