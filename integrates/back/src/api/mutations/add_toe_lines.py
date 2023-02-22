from .payloads.types import (
    SimplePayload,
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
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
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
from sessions import (
    domain as sessions_domain,
)
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToAdd,
)
from typing import (
    Any,
)


@MUTATION.field("addToeLines")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(  # pylint: disable=too-many-arguments
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    root_id: str,
    filename: str,
    last_author: str,
    last_commit: str,
    loc: int,
    modified_date: datetime,
    **_kwargs: Any,
) -> SimplePayload:
    try:
        loaders: Dataloaders = info.context.loaders
        user_data = await sessions_domain.get_jwt_content(info.context)
        user_email = user_data["user_email"]
        await toe_lines_domain.add(
            loaders=loaders,
            group_name=group_name,
            root_id=root_id,
            filename=filename,
            attributes=ToeLinesAttributesToAdd(
                attacked_lines=0,
                be_present=False,
                last_author=last_author,
                last_commit=last_commit,
                loc=loc,
                last_commit_date=modified_date,
                seen_first_time_by=user_email,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added toe lines in group {group_name} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to add toe lines in group {group_name}",
        )
        raise

    return SimplePayload(success=True)
