from .payloads.types import (
    UpdateToeLinesPayload,
)
from .schema import (
    MUTATION,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ToeLinesNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_lines.types import (
    ToeLinesRequest,
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
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
)
from typing import (
    Any,
)


@MUTATION.field("updateToeLinesAttackedLines")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    comments: str,
    filename: str,
    group_name: str,
    root_id: str,
    **kwargs: Any,
) -> UpdateToeLinesPayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        loaders: Dataloaders = info.context.loaders
        current_value = await loaders.toe_lines.load(
            ToeLinesRequest(
                filename=filename, group_name=group_name, root_id=root_id
            )
        )
        if current_value is None:
            raise ToeLinesNotFound()

        await toe_lines_domain.update(
            current_value,
            ToeLinesAttributesToUpdate(
                attacked_at=datetime_utils.get_utc_now(),
                attacked_by=user_email,
                attacked_lines=kwargs.get(
                    "attacked_lines", current_value.state.loc
                ),
                comments=comments,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Updated toe lines attacked lines "
            f"for group {group_name}, and root id {root_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Tried to update toe lines attacked lines "
            f"for group {group_name}, and root id {root_id}",
        )
        raise

    return UpdateToeLinesPayload(
        success=True, group_name=group_name, filename=filename, root_id=root_id
    )
