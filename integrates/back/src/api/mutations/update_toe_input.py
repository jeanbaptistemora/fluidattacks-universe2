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
    ToeInput,
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
    datetime as datetime_utils,
    logs as logs_utils,
    token as token_utils,
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
async def mutate(  # pylint: disable=too-many-arguments
    _parent: None,
    info: GraphQLResolveInfo,
    be_present: bool,
    component: str,
    entry_point: str,
    group_name: str,
    root_id: str,
    **kwargs: Any,
) -> SimplePayloadType:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        loaders: Dataloaders = info.context.loaders
        current_value: ToeInput = await loaders.toe_input.load(
            ToeInputRequest(
                component=component,
                entry_point=entry_point,
                group_name=group_name,
                root_id=root_id,
            )
        )
        be_present_to_update = (
            None if be_present is current_value.be_present else be_present
        )
        attacked_at_to_update = (
            datetime_utils.get_utc_now()
            if kwargs.get("has_recent_attack") is True
            else None
        )
        attacked_by_to_update = (
            None if attacked_at_to_update is None else user_email
        )
        await toe_inputs_domain.update(
            current_value,
            ToeInputAttributesToUpdate(
                attacked_at=attacked_at_to_update,
                attacked_by=attacked_by_to_update,
                be_present=be_present_to_update,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated toe input in group {group_name} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update toe input in group {group_name}",
        )
        raise

    return SimplePayloadType(success=True)
