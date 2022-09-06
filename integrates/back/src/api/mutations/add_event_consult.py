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
    logs as logs_utils,
    stakeholders as stakeholders_utils,
    token as token_utils,
    validations,
)
from newutils.datetime import (
    get_as_utc_iso_format,
    get_now,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from time import (
    time,
)
from typing import (
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    content: str,
    event_id: str,
    parent_comment: str,
) -> AddConsultPayload:
    validations.validate_fields([content])

    comment_id: str = str(round(time() * 1000))
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    today = get_as_utc_iso_format(get_now())
    user_email = str(user_info["user_email"])

    comment_data = EventComment(
        event_id=event_id,
        parent_id=str(parent_comment),
        creation_date=today,
        content=content,
        id=comment_id,
        email=user_email,
        full_name=stakeholders_utils.get_full_name(user_info),
    )
    await events_domain.add_comment(
        info, user_email, comment_data, event_id, parent_comment
    )

    redis_del_by_deps_soon("add_event_consult", event_id=event_id)

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added comment to event {event_id} successfully",
    )

    return AddConsultPayload(success=True, comment_id=str(comment_id))
