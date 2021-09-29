# This mutation updates the attribute sorts_file_risk for a concrete Toe


from aioextensions import (
    collect,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from decorators import (
    concurrent_decorators,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from toe.lines import (
    domain as toe_lines_domain,
)
from typing import (
    Any,
    List,
    Set,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(require_login, require_asm)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    filename: str,
    sorts_risk_level: float,
) -> SimplePayloadType:
    success = False
    group_toe_lines_loader = info.context.loaders.group_toe_lines
    group_toes: Set[ToeLines] = await group_toe_lines_loader.load(group_name)

    # Rare, but we can have the same filename in different roots.
    # That's why this set
    root_ids: Set[str] = set()
    group_toes_to_update: List[ToeLines] = []
    for toe in group_toes:
        if toe.filename == filename:
            toe = toe._replace(sorts_risk_level=sorts_risk_level)
            group_toes_to_update.append(toe)
            root_ids.add(toe.root_id)

    if group_toes_to_update:
        await collect(
            [toe_lines_domain.update(toe) for toe in group_toes_to_update]
        )
        success = True
        await collect(
            [
                redis_del_by_deps(
                    "update_toe_lines_sorts", group=group_name, root_id=root_id
                )
                for root_id in root_ids
            ]
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Successfully updated sorts risk level "
            f"for group {group_name} in toes with filename {filename}",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update sorts risk level "
            f"for group {group_name} in toes with filename {filename}",
        )

    return SimplePayloadType(success=success)
