from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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


@MUTATION.field("updateEvidenceDescription")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    evidence_id: str,
    description: str,
) -> SimplePayload:
    try:
        await findings_domain.update_evidence_description(
            loaders=info.context.loaders,
            finding_id=finding_id,
            evidence_id=evidence_id,
            description=description,
        )
        logs_utils.cloudwatch_log(
            info.context,
            (
                "Security: Evidence description successfully updated in "
                f"finding {finding_id}"
            ),
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            (
                "Security: Attempted to update evidence description in "
                f"{finding_id}"
            ),
        )
        raise

    return SimplePayload(success=True)
