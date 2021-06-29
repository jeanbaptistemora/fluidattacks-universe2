from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleFindingPayload,
    SimplePayload,
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
    require_finding_access,
    require_integrates,
    require_login,
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
    require_integrates,
    require_finding_access,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, finding_id: str, **kwags: Any
) -> SimplePayload:
    try:
        finding_loader = info.context.loaders.finding_new
        description = FindingDescriptionToUpdate(
            actor=kwags["actor"],
            affected_systems=kwags["affected_systems"],
            attack_vector_desc=kwags["attack_vector_desc"],
            compromised_attributes=kwags.get("records"),
            compromised_records=kwags["records_number"],
            cwe=kwags["cwe"],
            description=kwags["description"],
            recommendation=kwags["recommendation"],
            requirements=kwags["requirements"],
            risk=kwags.get("risk"),
            scenario=kwags["scenario"],
            sorts=FindingSorts[kwags["sorts"]] if kwags.get("sorts") else None,
            threat=kwags["threat"],
            title=kwags["title"],
            type=kwags.get("finding_type"),
        )
        await findings_domain.update_description_new(
            info.context, finding_id, description
        )
        redis_del_by_deps_soon(
            "update_finding_description_new",
            finding_new_id=finding_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated description in finding "
            f"{finding_id} with success",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update description in finding {finding_id}",
        )
        raise

    finding_loader.clear(finding_id)
    finding: Finding = await finding_loader.load(finding_id)
    return SimpleFindingPayload(finding=finding, success=True)
