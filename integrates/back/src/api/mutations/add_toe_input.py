from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
)
from typing import (
    Any,
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
    component: str,
    entry_point: str,
    group_name: str,
    root_id: str,
    **_kwargs: Any,
) -> SimplePayloadType:
    try:
        loaders: Dataloaders = info.context.loaders
        user_data = await token_utils.get_jwt_content(info.context)
        user_email = user_data["user_email"]
        await toe_inputs_domain.add(
            loaders=loaders,
            group_name=group_name,
            component=component,
            entry_point=entry_point,
            attributes=ToeInputAttributesToAdd(
                be_present=True,
                unreliable_root_id=root_id,
                has_vulnerabilities=False,
                seen_first_time_by=user_email,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Successfully added toe input in group {group_name}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to add toe input in group {group_name}",
        )
        raise

    return SimplePayloadType(success=True)
