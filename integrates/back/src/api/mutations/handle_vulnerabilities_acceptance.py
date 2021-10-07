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
    List,
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
    **parameters: Any,
) -> SimplePayload:
    accepted_vulnerabilities: List[str] = get_key_or_fallback(
        parameters, "accepted_vulnerabilities", "accepted_vulns"
    )
    rejected_vulnerabilities: List[str] = get_key_or_fallback(
        parameters, "rejected_vulnerabilities", "rejected_vulns"
    )
    user_info = await token_utils.get_jwt_content(info.context)
    email: str = user_info["user_email"]
    success: bool = await handle_vulnerabilities_acceptance(
        context=info.context.loaders,
        accepted_vulns=accepted_vulnerabilities,
        finding_id=finding_id,
        justification=justification,
        rejected_vulns=rejected_vulnerabilities,
        user_email=email,
    )
    if success:
        redis_del_by_deps_soon(
            "handle_vulnerabilities_acceptance",
            finding_id=finding_id,
        )

    return SimplePayload(success=success)
