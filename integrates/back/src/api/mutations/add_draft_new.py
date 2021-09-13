from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDraftToAdd,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@rename_kwargs({"project_name": "group_name"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    title: str,
    **kwargs: Any,
) -> SimplePayload:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        user_email = user_info["user_email"]
        draft_info = FindingDraftToAdd(
            affected_systems=kwargs.get("affected_systems"),
            hacker_email=user_email,
            attack_vector_description=kwargs.get("attack_vector_description")
            or kwargs.get("attack_vector_desc"),
            description=kwargs.get("description"),
            recommendation=kwargs.get("recommendation"),
            requirements=kwargs.get("requirements"),
            threat=kwargs.get("threat"),
            title=title,
            type=kwargs.get("type"),
        )
        await findings_domain.add_draft_new(
            info.context, group_name, user_email, draft_info
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created draft in {group_name} group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to create draft in {group_name} group",
        )
        raise
    return SimplePayload(success=True)
