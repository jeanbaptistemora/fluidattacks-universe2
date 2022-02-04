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
from db_model.toe_inputs.types import (
    ToeInputRequest,
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
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToUpdate,
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
    entry_point: str,
    component: str,
    group_name: str,
    seen_first_time_by: str,
    **_kwargs: Any,
) -> SimplePayloadType:
    try:
        loaders: Dataloaders = info.context.loaders
        current_value = await loaders.toe_input.load(
            ToeInputRequest(
                component=component,
                entry_point=entry_point,
                group_name=group_name,
            )
        )
        await toe_inputs_domain.update(
            current_value,
            attributes=ToeInputAttributesToUpdate(
                seen_first_time_by=seen_first_time_by
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Successfully enumerate toe input in group "
            f"{group_name}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to enumerate toe input in group {group_name}",
        )
        raise

    return SimplePayloadType(success=True)
