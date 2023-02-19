from .payloads.types import (
    UpdateToePortPayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ToePortNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_ports.types import (
    ToePortRequest,
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
)
from sessions import (
    domain as sessions_domain,
)
from toe.ports import (
    domain as toe_ports_domain,
)
from toe.ports.types import (
    ToePortAttributesToUpdate,
)
from typing import (
    Any,
)


@MUTATION.field("updateToePort")
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
    address: str,
    port: int,
    group_name: str,
    root_id: str,
    **kwargs: Any,
) -> UpdateToePortPayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email = user_info["user_email"]
        loaders: Dataloaders = info.context.loaders
        current_value = await loaders.toe_port.load(
            ToePortRequest(
                address=address,
                port=str(port),
                group_name=group_name,
                root_id=root_id,
            )
        )
        if current_value is None:
            raise ToePortNotFound()

        be_present_to_update = (
            None
            if be_present is current_value.state.be_present
            else be_present
        )
        attacked_at_to_update = (
            datetime_utils.get_utc_now()
            if kwargs.get("has_recent_attack") is True
            else None
        )
        attacked_by_to_update = (
            None if attacked_at_to_update is None else user_email
        )
        await toe_ports_domain.update(
            current_value=current_value,
            attributes=ToePortAttributesToUpdate(
                attacked_at=attacked_at_to_update,
                attacked_by=attacked_by_to_update,
                be_present=be_present_to_update,
            ),
            modified_by=user_email,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated toe port in group {group_name} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update toe port in group {group_name}",
        )
        raise

    return UpdateToePortPayload(
        address=address,
        port=str(port),
        group_name=group_name,
        root_id=root_id,
        success=True,
    )
