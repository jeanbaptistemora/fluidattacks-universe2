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
from db_model.roots.types import (
    RootItem,
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
from roots import (
    domain as roots_domain,
)
from toe.services_lines import (
    domain as toe_lines_domain,
)
from typing import (
    Any,
    Tuple,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(require_login, require_asm)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    root_nickname: str,
    filename: str,
    sorts_risk_level: float,
) -> SimplePayloadType:
    try:
        group_roots_loader = info.context.loaders.group_roots
        roots: Tuple[RootItem, ...] = await group_roots_loader.load(group_name)
        root_id = roots_domain.get_root_id_by_nickname(root_nickname, roots)
        await toe_lines_domain.update_risk_level(
            group_name=group_name,
            filename=filename,
            root_id=root_id,
            sorts_risk_level=sorts_risk_level,
        )
        redis_del_by_deps(
            "update_toe_lines_sorts", group=group_name, root_id=root_id
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
