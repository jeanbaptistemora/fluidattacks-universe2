from api.mutations import (
    AddConsultPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.event_comments.types import (
    EventComment,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
    stakeholders as stakeholders_utils,
)
from sessions import (
    domain as sessions_domain,
)
from time import (
    time,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    content: str,
    event_id: str,
    parent_comment: str,
) -> AddConsultPayload:

    comment_id: str = str(round(time() * 1000))
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    email = str(user_info["user_email"])

    comment_data = EventComment(
        event_id=event_id,
        parent_id=str(parent_comment),
        creation_date=datetime_utils.get_utc_now(),
        content=content,
        id=comment_id,
        email=email,
        full_name=stakeholders_utils.get_full_name(user_info),
    )
    await events_domain.add_comment(
        loaders=info.context.loaders,
        comment_data=comment_data,
        email=email,
        event_id=event_id,
        parent_comment=parent_comment,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added comment to event {event_id} successfully",
    )

    return AddConsultPayload(success=True, comment_id=str(comment_id))
