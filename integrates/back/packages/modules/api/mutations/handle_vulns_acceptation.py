
from typing import List

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from newutils import token as token_utils
from redis_cluster.operations import redis_del_by_deps_soon
from vulnerabilities.domain import handle_vulns_acceptation


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    accepted_vulns: List[str],
    rejected_vulns: List[str],
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    email: str = user_info['user_email']
    success: bool = await handle_vulns_acceptation(
        context=info.context.loaders,
        accepted_vulns=accepted_vulns,
        finding_id=finding_id,
        justification=justification,
        rejected_vulns=rejected_vulns,
        user_email=email,
    )
    if success:
        redis_del_by_deps_soon(
            'handle_vulns_acceptation',
            finding_id=finding_id,
        )

    return SimplePayload(success=success)
