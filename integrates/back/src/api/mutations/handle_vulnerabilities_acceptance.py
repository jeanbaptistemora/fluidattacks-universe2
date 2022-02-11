from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
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
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    List,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities.domain import (
    handle_vulnerabilities_acceptance,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    accepted_vulnerabilities: List[str],
    rejected_vulnerabilities: List[str],
) -> SimplePayload:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        email: str = user_info["user_email"]
        await handle_vulnerabilities_acceptance(
            loaders=info.context.loaders,
            accepted_vulns=accepted_vulnerabilities,
            finding_id=finding_id,
            justification=justification,
            rejected_vulns=rejected_vulnerabilities,
            user_email=email,
        )
        redis_del_by_deps_soon(
            "handle_vulnerabilities_acceptance",
            finding_id=finding_id,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.handle_vulnerabilities_acceptance,
            finding_ids=[finding_id],
            vulnerability_ids=accepted_vulnerabilities
            + rejected_vulnerabilities,
        )
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Handled vulnerabilities acceptance in finding "
            f"{finding_id}",
        )

    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to handle vulnerabilities acceptance in "
            f"finding {finding_id}",
        )
        raise

    return SimplePayload(success=True)
