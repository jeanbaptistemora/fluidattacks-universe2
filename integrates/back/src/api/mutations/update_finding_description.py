from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimpleFindingPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.findings.enums import (
    FindingSorts,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDescriptionToUpdate,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    validations,
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
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, finding_id: str, **kwargs: Any
) -> SimpleFindingPayload:
    try:
        finding_loader = info.context.loaders.finding
        old_finding: Finding = await finding_loader.load(finding_id)
        validations.validate_finding_title_change_policy(
            old_title=old_finding.title,
            new_title=kwargs["title"],
            status=old_finding.state.status,
        )

        description = FindingDescriptionToUpdate(
            attack_vector_description=kwargs["attack_vector_description"],
            description=kwargs["description"],
            recommendation=kwargs["recommendation"],
            sorts=FindingSorts[kwargs["sorts"]]
            if kwargs.get("sorts")
            else None,
            threat=kwargs["threat"],
            title=kwargs["title"],
        )
        await findings_domain.update_description(
            info.context.loaders, finding_id, description
        )
        redis_del_by_deps_soon(
            "update_finding_description",
            finding_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated description in finding "
            f"{finding_id} with success",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to update description in finding "
            f"{finding_id}",
        )
        raise

    finding_loader.clear(finding_id)
    finding = await finding_loader.load(finding_id)
    return SimpleFindingPayload(finding=finding, success=True)
