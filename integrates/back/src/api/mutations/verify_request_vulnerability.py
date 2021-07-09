from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayloadType:
    finding_id = parameters.get("finding_id", "")
    user_info = await token_utils.get_jwt_content(info.context)
    success = await findings_domain.verify_vulnerabilities(
        info=info,
        finding_id=finding_id,
        user_info=user_info,
        parameters=parameters,
        vulns_to_close_from_file=[],
    )
    if success:
        finding_loader = info.context.loaders.finding
        finding_data = await finding_loader.load(finding_id)
        group_name = get_key_or_fallback(finding_data)
        redis_del_by_deps_soon(
            "verify_request_vulnerability",
            finding_id=finding_id,
            group_name=group_name,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Verified a request in finding_id: {finding_id}",
        )

    return SimplePayloadType(success=success)
