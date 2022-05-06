# This mutation updates the attribute sorts_file_risk for a concrete Toe


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
from db_model.roots.types import (
    Root,
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
from roots import (
    domain as roots_domain,
)
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
)
from typing import (
    Any,
    Tuple,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    root_nickname: str,
    filename: str,
    sorts_risk_level: int,
) -> SimplePayloadType:
    try:
        loaders: Dataloaders = info.context.loaders
        roots: Tuple[Root, ...] = await loaders.group_roots.load(group_name)
        root_id = roots_domain.get_root_id_by_nickname(
            root_nickname, roots, only_git_roots=True
        )
        toe_lines: ToeLines = await loaders.toe_lines.load(
            ToeLinesRequest(
                filename=filename, group_name=group_name, root_id=root_id
            )
        )
        await toe_lines_domain.update(
            toe_lines,
            ToeLinesAttributesToUpdate(sorts_risk_level=sorts_risk_level),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated sorts risk level for group {group_name} in "
            f"toes with filename {filename} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update sorts risk level "
            f"for group {group_name} in toes with filename {filename}",
        )
        raise

    return SimplePayloadType(success=True)
