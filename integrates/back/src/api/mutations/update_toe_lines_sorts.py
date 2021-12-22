# This mutation updates the attribute sorts_file_risk for a concrete Toe


from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    ToeLinesNotFound,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    RootItem,
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
from toe.services_lines import (
    domain as services_toe_lines_domain,
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
        roots: Tuple[RootItem, ...] = await loaders.group_roots.load(
            group_name
        )
        root_id = roots_domain.get_root_id_by_nickname(root_nickname, roots)
        with suppress(ToeLinesNotFound):
            toe_lines: ToeLines = await loaders.toe_lines.load(
                ToeLinesRequest(
                    filename=filename, group_name=group_name, root_id=root_id
                )
            )
            await toe_lines_domain.update(
                toe_lines,
                ToeLinesAttributesToUpdate(sorts_risk_level=sorts_risk_level),
            )
        with suppress(ToeLinesNotFound):
            await services_toe_lines_domain.update_risk_level(
                group_name=group_name,
                filename=filename,
                root_id=root_id,
                sorts_risk_level=sorts_risk_level,
            )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Successfully updated sorts risk level "
            f"for group {group_name} in toes with filename {filename}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update sorts risk level "
            f"for group {group_name} in toes with filename {filename}",
        )
        raise

    return SimplePayloadType(success=True)
