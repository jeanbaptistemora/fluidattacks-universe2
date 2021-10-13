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
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from starlette.datastructures import (
    UploadFile,
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
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    try:
        file: UploadFile = kwargs["file"]
        finding_id: str = kwargs["finding_id"]
        evidence_id: str = kwargs["evidence_id"]
        await findings_domain.update_evidence(
            info.context.loaders, finding_id, evidence_id, file
        )
        redis_del_by_deps_soon(
            "update_evidence",
            finding_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated evidence in finding {finding_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to update evidence in finding {finding_id}",
        )
        raise
    return SimplePayload(success=True)
