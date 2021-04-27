# This mutation updates the attribute sorts_file_risk for a concrete Toe

# Standard library
from typing import (
    Any,
    List,
    Tuple
)

# Third party libraries
from aioextensions import collect
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import (
    concurrent_decorators,
    require_integrates,
    require_login
)
from backend.typing import SimplePayload as SimplePayloadType
from data_containers.toe_lines import GitRootToeLines
from toe.lines import domain as toe_lines_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    require_integrates
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    filename: str,
    sorts_risk_level: float
) -> SimplePayloadType:
    success = False
    group_toes: Tuple[GitRootToeLines, ...] = \
        await toe_lines_domain.get_by_group(group_name)

    group_toes_to_update: List[GitRootToeLines] = []
    for toe in group_toes:
        if toe.filename == filename:
            toe = toe._replace(sorts_risk_level=sorts_risk_level)
            group_toes_to_update.append(toe)
    if group_toes_to_update:
        await collect([
            toe_lines_domain.update(toe)
            for toe in group_toes_to_update
        ])
        success = True
        util.cloudwatch_log(
            info.context,
            f'Security: Successfully updated sorts risk level '
            f'for group {group_name} in toes with filename {filename}',
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Tried to update sorts risk level '
            f'for group {group_name} in toes with filename {filename}',
        )

    return SimplePayloadType(success=success)
