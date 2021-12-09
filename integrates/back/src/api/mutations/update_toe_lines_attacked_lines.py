from aioextensions import (
    collect,
)
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
from db_model.toe_lines.types import (
    ToeLines,
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
    logs as logs_utils,
)
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
)
from typing import (
    List,
    Tuple,
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
    attacked_lines: int,
    attacked_at: str,
    comments: str,
    filenames: List[str],
    group_name: str,
    root_id: str,
) -> SimplePayloadType:
    try:
        loaders: Dataloaders = info.context.loaders
        toe_lines: Tuple[ToeLines, ...] = await loaders.toe_lines.load_many(
            [
                ToeLinesRequest(
                    filename=filename, group_name=group_name, root_id=root_id
                )
                for filename in filenames
            ]
        )
        await collect(
            tuple(
                toe_lines_domain.update(
                    curren_value,
                    ToeLinesAttributesToUpdate(
                        attacked_at=attacked_at,
                        attacked_lines=attacked_lines,
                        comments=comments,
                    ),
                )
                for curren_value in toe_lines
            )
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Successfully updated toe lines attacked lines "
            f"for group {group_name}, and root id {root_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update toe lines attacked lines "
            f"for group {group_name}, and root id {root_id}",
        )
        raise

    return SimplePayloadType(success=True)
