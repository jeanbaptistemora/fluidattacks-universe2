from .payloads.types import (
    AddConsultPayload,
)
from .schema import (
    MUTATION,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.group_comments.types import (
    GroupComment,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_squad,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_comments import (
    domain as group_comments_domain,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)
import time
from typing import (
    Any,
)


@MUTATION.field("addGroupConsult")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_squad,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str, **parameters: Any
) -> AddConsultPayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    comment_id = int(round(time.time() * 1000))
    content = parameters["content"]
    comment_data = GroupComment(
        group_name=group_name,
        id=str(comment_id),
        content=content,
        creation_date=datetime_utils.get_utc_now(),
        full_name=str.join(
            " ", [user_info["first_name"], user_info["last_name"]]
        ),
        parent_id=str(parameters.get("parent_comment")),
        email=user_email,
    )
    await group_comments_domain.add_comment(
        loaders=loaders, group_name=group_name, comment_data=comment_data
    )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added comment to {group_name} group successfully",
    )

    return AddConsultPayload(success=True, comment_id=str(comment_id))
