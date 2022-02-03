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
        await toe_inputs_domain.remove(current_value)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Successfully removed toe input from group "
            f"{group_name}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to removed toe input from  group {group_name}",
        )
        raise

    return SimplePayloadType(success=True)
